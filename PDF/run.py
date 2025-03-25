import streamlit as st
from fpdf import FPDF
import base64
import tempfile
import os
from io import BytesIO

# 📌 한글 폰트 경로 (NanumGothic.ttf, NanumGothicBold.ttf 필요)
FONT_PATH = "./NanumGothic.ttf"
BOLD_FONT_PATH = "./NanumGothicBold.ttf"


class MarketingReport(FPDF):
    def header(self):
        """헤더: 마케팅 보고서 제목"""
        self.set_font("NanumGothic", "B", 16)  # ✅ 굵은 폰트 사용
        self.cell(0, 10, "📊 2024 마케팅 성과 보고서", ln=True, align="C")
        self.ln(5)

    def footer(self):
        """푸터: 페이지 번호 표시"""
        self.set_y(-15)
        self.set_font("NanumGothic", size=10)
        self.cell(0, 10, f"페이지 {self.page_no()}", align="C")


def generate_pdf():
    pdf = MarketingReport()

    # ✅ add_page() 전에 폰트 추가
    pdf.add_font("NanumGothic", "", FONT_PATH, uni=True)
    pdf.add_font("NanumGothic", "B", BOLD_FONT_PATH, uni=True)

    pdf.add_page()
    pdf.set_font("NanumGothic", size=12)

    # 📌 보고서 개요
    pdf.set_font("NanumGothic", "B", 14)
    pdf.cell(0, 10, "📌 개요", ln=True)

    pdf.set_font("NanumGothic", size=12)
    pdf.multi_cell(
        0,
        8,
        "이 보고서는 2024년 1분기 마케팅 성과를 분석하며, 주요 매출 데이터와 트렌드를 포함하고 있습니다.",
    )

    pdf.ln(5)

    # 📊 매출 데이터 표
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("NanumGothic", "B", 12)
    pdf.cell(50, 10, "월", border=1, fill=True)
    pdf.cell(50, 10, "매출 ($)", border=1, fill=True)
    pdf.cell(50, 10, "전환율", border=1, fill=True)
    pdf.ln()

    pdf.set_font("NanumGothic", size=12)
    data = [
        ("1월", "50,000", "2.5%"),
        ("2월", "60,000", "3.1%"),
        ("3월", "75,000", "3.8%"),
        ("4월", "90,000", "4.5%"),
    ]

    for row in data:
        for col in row:
            pdf.cell(50, 10, col, border=1)
        pdf.ln()

    pdf.ln(5)

    # ✅ 주요 성과
    pdf.set_font("NanumGothic", "B", 14)
    pdf.cell(0, 10, "✅ 주요 성과", ln=True)

    pdf.set_font("NanumGothic", size=12)
    achievements = [
        "📈 35% 증가한 SNS 참여율",
        "💰 20% 증가한 온라인 매출",
        "📊 고객 유지율 15% 향상",
        "🤝 인플루언서 협업 성공",
    ]

    for point in achievements:
        pdf.cell(0, 8, point, ln=True)

    # 📄 PDF를 BytesIO로 저장
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output


# 📌 Streamlit에서 PDF 미리 보기
def show_pdf(pdf_output):
    pdf_base64 = base64.b64encode(pdf_output.read()).decode("utf-8")
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>',
        unsafe_allow_html=True,
    )


# 📌 Streamlit UI
def main():
    st.title("📊 마케팅 보고서 PDF 생성기")
    st.write("2024년 마케팅 성과 보고서를 PDF로 생성하고 미리 보기합니다.")

    if st.button("📄 PDF 생성 & 미리 보기"):
        pdf_output = generate_pdf()
        show_pdf(pdf_output)

        # 📥 다운로드 버튼
        st.download_button(
            label="📥 PDF 다운로드",
            data=pdf_output.getvalue(),
            file_name="marketing_report.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
