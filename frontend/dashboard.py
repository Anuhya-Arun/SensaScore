import streamlit as st
import requests
import pandas as pd
import time

# Backend URL
BACKEND_URL = "http://localhost:5000"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        color: #2ca02c;
        font-size: 1.5em;
        margin-top: 30px;
    }
    .metric-card {
        padding: 15px;
        border-radius: 10px;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-msg {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="SensaScore - Headline Sensationalism Analyzer", page_icon="📰")

st.markdown('<h1 class="main-header">📰 SensaScore</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2em; color: #666;">Analyze news headlines for sensationalism on a scale of 0-4</p>', unsafe_allow_html=True)

# Check backend health
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Single headline analysis
st.markdown('<h2 class="sub-header">Single Headline Analysis</h2>', unsafe_allow_html=True)

headline_input = st.text_input("Enter a news headline:", placeholder="e.g., Unbelievable discovery shocks scientists!", key="headline_input")

if st.button("Analyze Headline", type="primary", use_container_width=True):
    if not headline_input.strip():
        st.error("Please enter a headline")
    elif not check_backend():
        st.error("Backend service is not running. Please start the Flask server.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/predict",
                    json={"headline": headline_input},
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display results in a nice layout
                    st.success("Analysis Complete!")
                    
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Sensationalism Score", f"{result['score']}/4")
                        
                        # Score interpretation with colors
                        if result['score'] < 1:
                            st.markdown('<div class="success-msg">✅ Factual & Neutral</div>', unsafe_allow_html=True)
                        elif result['score'] < 2:
                            st.markdown('<div class="warning-msg">ℹ️ Slightly Attention-Grabbing</div>', unsafe_allow_html=True)
                        elif result['score'] < 3:
                            st.markdown('<div class="warning-msg">⚠️ Moderately Sensational</div>', unsafe_allow_html=True)
                        elif result['score'] < 4:
                            st.markdown('<div class="error-msg">🚨 Highly Sensational</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-msg">💥 Extreme Clickbait</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.subheader("Why this score?")
                        for reason in result['explanation']:
                            st.write(f"• {reason}")

                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. The analysis might be taking longer due to AI processing.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Batch analysis
st.markdown('<h2 class="sub-header">Batch Analysis</h2>', unsafe_allow_html=True)
st.markdown("Upload a CSV file with headlines to analyze multiple at once")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="File must contain a 'headline' column")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        if 'headline' not in df.columns:
            st.error("CSV file must contain a 'headline' column")
        else:
            st.write(f"📊 Loaded {len(df)} headlines")
            st.dataframe(df.head(), use_container_width=True)

            if st.button("Analyze All Headlines", type="primary", use_container_width=True):
                if not check_backend():
                    st.error("Backend service is not running. Please start the Flask server.")
                else:
                    with st.spinner("Analyzing headlines... This may take a while for large files."):
                        try:
                            # Prepare file for upload
                            files = {'file': ('headlines.csv', uploaded_file.getvalue(), 'text/csv')}

                            response = requests.post(
                                f"{BACKEND_URL}/api/batch_predict",
                                files=files,
                                timeout=300  # 5 minutes timeout
                            )

                            if response.status_code == 200:
                                batch_result = response.json()

                                # Summary
                                st.success("Batch Analysis Complete!")
                                summary = batch_result['summary']
                                
                                st.subheader("📈 Summary Statistics")
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Total Headlines", summary['total_headlines'])
                                with col2:
                                    st.metric("Average Score", f"{summary['average_score']:.2f}/4")
                                with col3:
                                    high_risk = summary['score_distribution']['3'] + summary['score_distribution']['4']
                                    st.metric("High Risk (3+)", high_risk)

                                # Distribution chart
                                st.subheader("📊 Score Distribution")
                                dist_data = summary['score_distribution']
                                st.bar_chart(dist_data)

                                # Results table (remove rewritten column)
                                st.subheader("📋 Detailed Results")
                                results_df = pd.DataFrame(batch_result['results'])
                                # Remove the rewritten column
                                if 'rewritten' in results_df.columns:
                                    results_df = results_df.drop('rewritten', axis=1)
                                st.dataframe(results_df, use_container_width=True)

                                # Download results
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Results as CSV",
                                    data=csv,
                                    file_name="sensascore_results.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )

                            else:
                                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

                        except requests.exceptions.Timeout:
                            st.error("Request timed out. Try with a smaller file or check backend logs.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                        try:
                            # Prepare file for upload
                            files = {'file': ('headlines.csv', uploaded_file.getvalue(), 'text/csv')}

                            response = requests.post(
                                f"{BACKEND_URL}/api/batch_predict",
                                files=files,
                                timeout=300  # 5 minutes timeout
                            )

                            if response.status_code == 200:
                                batch_result = response.json()

                                # Summary
                                st.subheader("Summary Statistics")
                                summary = batch_result['summary']
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Total Headlines", summary['total_headlines'])
                                with col2:
                                    st.metric("Average Score", f"{summary['average_score']}/4")
                                with col3:
                                    st.metric("High Risk (3+)", summary['score_distribution']['3-4'] + summary['score_distribution']['4'])

                                # Distribution chart
                                st.subheader("Score Distribution")
                                dist_data = summary['score_distribution']
                                st.bar_chart(dist_data)

                                # Results table
                                st.subheader("Detailed Results")
                                results_df = pd.DataFrame(batch_result['results'])
                                st.dataframe(results_df)

                                # Download results
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="Download Results as CSV",
                                    data=csv,
                                    file_name="sensascore_results.csv",
                                    mime="text/csv"
                                )

                            else:
                                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

                        except requests.exceptions.Timeout:
                            st.error("Request timed out. Try with a smaller file or check backend logs.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**About SensaScore:** This system analyzes news headlines for sensationalism using machine learning and AI. Scores range from 0 (factual) to 4 (extreme clickbait).")

# Instructions
with st.expander("How to use"):
    st.markdown("""
    **Single Analysis:**
    - Enter any news headline in the text box
    - Click "Analyze Headline" to get score, explanation, and neutral rewrite

    **Batch Analysis:**
    - Prepare a CSV file with a column named 'headline'
    - Upload the file and click "Analyze All Headlines"
    - Get summary statistics and detailed results

    **Score Guide:**
    - 0-1: Factual and neutral
    - 1-2: Slightly attention-grabbing
    - 2-3: Moderately sensational
    - 3-4: Highly sensational
    - 4: Extreme clickbait
    """)

# Backend status
backend_status = "🟢 Running" if check_backend() else "🔴 Not Running"
st.sidebar.markdown(f"**Backend Status:** {backend_status}")
if not check_backend():
    st.sidebar.warning("Start the Flask backend with: `python backend/app.py`")