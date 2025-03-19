import streamlit as st
from file_uploader import file_uploader
from data_display import display_data_preview, display_statistics
from filter import filter_data
from chart import plot_histogram, plot_bar_chart
from download import download_filtered_data


def main():
    st.title("CSV 파일 업로드 및 데이터 분석")

    # 1. 파일 업로드 (Input)
    df = file_uploader()

    # 파일이 업로드되었으면 실행
    if df is not None:
        # 2. 데이터 미리보기 출력 (Output)
        display_data_preview(df)

        # 3. 데이터 통계 출력 (Output)
        display_statistics(df)

        # 4. 특정 열 선택 (Input) 및 필터링 (Input)
        selected_column = st.selectbox("분석할 열을 선택하세요:", df.columns)
        st.write(f"선택된 열: {selected_column}")

        filtered_df = filter_data(df, selected_column)
        st.write("### 필터링된 데이터")
        st.write(filtered_df)

        # 5. 차트 시각화 (Output - Histogram)
        plot_histogram(filtered_df, selected_column)

        # 6. 추가 차트 시각화 (Output - Bar Chart)
        bar_column = st.selectbox("막대 차트를 위한 열을 선택하세요:", df.columns)
        plot_bar_chart(df, bar_column)

        # 7. 다운로드 버튼 (Output) - 분석된 데이터를 CSV로 다운로드
        download_filtered_data(filtered_df)


if __name__ == "__main__":
    main()
