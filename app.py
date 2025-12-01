#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FST Time NLU Web Demo
基于 Streamlit 的时间表达式识别演示应用
"""

import streamlit as st
from datetime import datetime
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chinese.fst_time_extractor import FstTimeExtractor as ChineseExtractor  # noqa: E402
from src.english.fst_time_extractor import FstTimeExtractor as EnglishExtractor  # noqa: E402


# 页面配置
st.set_page_config(
    page_title="FST Time NLU", page_icon="⏰", layout="wide", initial_sidebar_state="collapsed"
)

# 自定义CSS - 紧凑布局
st.markdown(
    """
<style>
    /* 减少整体间距 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 95%;
    }

    /* 标题 */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    /* 时间卡片 - 紧凑 */
    .time-point, .time-range {
        background: white;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .time-point {
        border-left: 3px solid #667eea;
    }
    .time-range {
        border-left: 3px solid #f5576c;
    }

    /* 时间显示 */
    .time-display {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        font-family: 'Monaco', 'Menlo', monospace;
    }
    .time-label {
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }

    /* 减少标题间距 */
    h1, h2, h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* 按钮 */
    .stButton>button {
        border-radius: 0.5rem;
        font-weight: 600;
    }

    /* 输入框 */
    .stTextArea textarea {
        border-radius: 0.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 初始化提取器（使用缓存）
@st.cache_resource
def get_extractors():
    """初始化并缓存提取器"""
    chinese_extractor = ChineseExtractor(overwrite_cache=False)
    english_extractor = EnglishExtractor(overwrite_cache=False)
    return chinese_extractor, english_extractor


def format_time_display(time_str):
    """格式化时间显示"""
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return time_str


def display_time_result(result, idx):
    """显示单个时间结果 - 紧凑版"""
    if isinstance(result, list):
        if len(result) == 2:
            # 时间段
            st.markdown(
                f"""
            <div class="time-range">
                <div style="font-weight: bold; color: #f5576c; margin-bottom: 0.5rem;">
                    ⏰ 时间段 {idx}
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="flex: 1;">
                        <div class="time-label">开始</div>
                        <div class="time-display">{format_time_display(result[0])}</div>
                    </div>
                    <div style="color: #999;">→</div>
                    <div style="flex: 1;">
                        <div class="time-label">结束</div>
                        <div class="time-display">{format_time_display(result[1])}</div>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        elif len(result) == 1:
            # 单个时间点
            st.markdown(
                f"""
            <div class="time-point">
                <div style="font-weight: bold; color: #667eea; margin-bottom: 0.5rem;">
                    📍 时间点 {idx}
                </div>
                <div class="time-display">{format_time_display(result[0])}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        # 单个时间点（字符串格式）
        st.markdown(
            f"""
        <div class="time-point">
            <div style="font-weight: bold; color: #667eea; margin-bottom: 0.5rem;">
                📍 时间点 {idx}
            </div>
            <div class="time-display">{format_time_display(result)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def main():  # noqa: C901
    # 标题
    st.markdown('<div class="main-header">⏰ FST Time NLU</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">基于有限状态转换器的时间表达式识别与解析</div>',
        unsafe_allow_html=True,
    )

    # 获取提取器
    chinese_extractor, english_extractor = get_extractors()

    # ==================== 紧凑的两栏布局 ====================
    col_left, col_right = st.columns([1.2, 1], gap="medium")

    with col_left:
        # 配置 + 输入
        col_config1, col_config2, col_config3, col_config4 = st.columns([1.5, 1.5, 1.5, 1.5])

        with col_config1:
            language = st.selectbox("🌍 语言", ["中文", "English"], index=0)

        with col_config2:
            base_date = st.date_input("📅 日期", datetime.now())

        with col_config3:
            base_time = st.time_input("🕐 时间", datetime.now().time())

        with col_config4:
            # 示例选择
            if language == "中文":
                examples = [
                    "明天上午9点",
                    "下下下周一",
                    "大概六天后的3时1刻需要处理东西",
                    "从明天9点到下午5点",
                    "明年母亲节",
                    "腊月18",
                    "6月第3个星期日",
                    "今晚八点30到明天上午",
                ]
            else:
                examples = [
                    "tomorrow at 9 AM",
                    "three Mondays from now",
                    "day after tomorrow 5pm",
                    "from 9:30 - 11:00 on Thursday",
                    "next thanksgiving day",
                    "the 80s",
                    "first tuesday of october",
                    "in a couple of minutes",
                ]

            # 初始化 session state
            if "last_example" not in st.session_state:
                st.session_state.last_example = ""

            selected_example = st.selectbox(
                "💡 示例",
                [""] + examples,
                format_func=lambda x: "选择示例..." if x == "" else x,
                key="example_selector",
            )

            # 只在示例改变时更新输入框
            if selected_example and selected_example != st.session_state.last_example:
                st.session_state.query_input = selected_example
                st.session_state.last_example = selected_example
            elif not selected_example:
                st.session_state.last_example = ""

        base_time_str = f"{base_date.strftime('%Y-%m-%d')}T{base_time.strftime('%H:%M:%S')}Z"

        # 输入区域
        query_text = st.text_area(
            "📝 输入文本",
            height=120,
            placeholder=(
                "请输入包含时间表达式的文本..."
                if language == "中文"
                else "Enter text with time expressions..."
            ),
            key="query_input",
        )

        # 操作按钮
        extract_button = st.button("🚀 识别时间", type="primary", use_container_width=True)

    with col_right:
        # 输出区域
        st.markdown("### 📊 识别结果")

        if extract_button and query_text:
            with st.spinner("⏳ 识别中..."):
                try:
                    extractor = chinese_extractor if language == "中文" else english_extractor
                    datetime_results, query_tag = extractor.extract(
                        query_text, base_time=base_time_str
                    )

                    if datetime_results:
                        # 简洁的统计
                        col_s1, col_s2 = st.columns(2)
                        col_s1.metric("✅ 识别数量", len(datetime_results))
                        col_s2.metric("📝 文本长度", len(query_text))

                        st.markdown("---")

                        # 显示时间
                        for idx, result in enumerate(datetime_results, 1):
                            display_time_result(result, idx)

                        # 详细信息
                        with st.expander("🔍 详细信息"):
                            tab1, tab2 = st.tabs(["JSON", "标签"])
                            with tab1:
                                st.json(
                                    {
                                        "query": query_text,
                                        "language": "chinese" if language == "中文" else "english",
                                        "base_time": base_time_str,
                                        "results": datetime_results,
                                    }
                                )
                            with tab2:
                                if query_tag:
                                    st.json(query_tag)
                                else:
                                    st.info("无标签")
                    else:
                        st.warning("⚠️ 未识别到时间表达式")
                        st.info("💡 请输入包含明确时间信息的文本")

                except Exception as e:
                    st.error(f"❌ 错误: {str(e)}")

        elif extract_button:
            st.warning("⚠️ 请先输入文本")
        else:
            st.info("👈 在左侧输入文本并点击「识别时间」")

    # 简洁的页脚
    with st.expander("ℹ️ 关于"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🚀 特性**\n- ⚡ ~4ms\n- 🎯 95%+\n- 🌏 中英文")
        with col2:
            st.markdown("**📚 文档**\n- [GitHub](https://github.com/y00281951/fst-time-nlu)")
        with col3:
            st.markdown("**📄 许可证**\n- Apache 2.0")


if __name__ == "__main__":
    main()
