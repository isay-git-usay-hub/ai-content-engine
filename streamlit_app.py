import streamlit as st
import asyncio
import pandas as pd
from app.logic import get_trends, generate_strategy, fetch_competitor_data, clear_trends_cache

# Page configuration
st.set_page_config(
    page_title="AI Content Strategy Engine",
    page_icon="🚀",
    layout="wide"
)

# --- Page Rendering Functions ---

def render_home_page():
    """Renders the welcome page."""
    st.title("🚀 Welcome to the AI Content Strategy Engine")
    st.markdown("""
    This application leverages AI and real-time data to help you discover trending topics and automatically generate content strategies.

    **Select a tool from the sidebar to begin:**
    - **Trend Dashboard:** View real-time trending topics from Google and Reddit.
    - **AI Content Strategy:** Generate a complete 30-day content plan based on current trends.
    - **Competitor Analysis:** Get insights into your competitors' social media activity (mock data).
    """)

async def render_trend_dashboard():
    """Renders the page for displaying trends."""
    st.title("📈 Trend Dashboard")
    st.markdown("Discover what's currently trending on Google and Reddit.")

    with st.spinner("🔍 Fetching the latest trends... this might take a moment."):
        trending_data = await get_trends()

    if not trending_data:
        st.error("😔 Could not fetch trending data at the moment. Please try again later or clear the cache.")
        return

    st.success(f"✅ Data fetched successfully! Last updated: {trending_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Google Trends")
        if trending_data.google_trends:
            google_df = pd.DataFrame.from_records(trending_data.google_trends)
            # Ensure required columns exist, fill with defaults if not
            if 'url' not in google_df.columns:
                google_df['url'] = '#'
            google_df['display_title'] = google_df.apply(lambda row: f"[{row['title']}]({row['url']})", axis=1)

            st.dataframe(
                google_df[['display_title', 'engagement_score']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "display_title": st.column_config.LinkColumn("Title", help="Click to see the Google Trend page.", max_chars=100),
                    "engagement_score": st.column_config.NumberColumn("Engagement", help="A score representing relative popularity."),
                },
            )
        else:
            st.warning("No Google Trends data available.")

    with col2:
        st.subheader("Reddit Trends")
        if trending_data.reddit_trends:
            reddit_df = pd.DataFrame.from_records(trending_data.reddit_trends)
            if 'url' not in reddit_df.columns:
                reddit_df['url'] = '#'
            reddit_df['display_title'] = reddit_df.apply(lambda row: f"[{row['title']}]({row['url']})", axis=1)
            reddit_df['subreddit'] = reddit_df.apply(lambda row: row.get('metadata', {}).get('subreddit', 'N/A'), axis=1)

            st.dataframe(
                reddit_df[['display_title', 'subreddit', 'engagement_score']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "display_title": st.column_config.LinkColumn("Title", help="Click to see the Reddit post.", max_chars=100),
                    "subreddit": st.column_config.TextColumn("Subreddit"),
                    "engagement_score": st.column_config.NumberColumn("Score", help="The Reddit score for the post."),
                },
            )
        else:
            st.warning("No Reddit Trends data available.")


async def render_ai_strategy_page():
    """Renders the page for generating AI content strategies."""
    st.title("🤖 AI Content Strategy Generator")
    st.markdown("Provide some details about your target audience and niche, and the AI will generate a content strategy based on the latest trends.")

    with st.form("strategy_form"):
        target_audience = st.text_input("Target Audience", help="Describe your ideal audience.", placeholder="e.g., Tech enthusiasts, small business owners")
        niche = st.text_input("Niche / Industry", help="What industry or topic area are you focused on?", placeholder="e.g., Artificial Intelligence, Sustainable Fashion")
        submitted = st.form_submit_button("✨ Generate Strategy")

    if submitted:
        if not target_audience or not niche:
            st.warning("Please fill in both the Target Audience and Niche fields.")
            return

        with st.spinner("🧠 AI is analyzing trends and crafting your strategy... this may take a minute."):
            strategy_response = await generate_strategy(target_audience, niche)

        if not strategy_response:
            st.error("😔 Could not generate a strategy at this time. This could be due to an issue with fetching trends or the AI service. Please try again later.")
        else:
            st.success("🎉 Your content strategy is ready!")

            st.subheader("📝 Analysis Summary")
            st.markdown(strategy_response.analysis_summary)

            st.subheader("🔥 Top Trends Used for Analysis")
            try:
                trends_df = pd.DataFrame([t.dict() for t in strategy_response.top_trends])
                st.dataframe(trends_df[['title', 'platform']], use_container_width=True, hide_index=True)
            except Exception as e:
                st.warning("Could not display top trends.")
                print(e)


            st.subheader("🗓️ Your Content Calendar")
            if not strategy_response.content_strategy:
                st.warning("The AI did not return any specific content recommendations.")
            else:
                for i, recommendation in enumerate(strategy_response.content_strategy):
                    with st.expander(f"**Day {i+1}: {recommendation.title}** on {recommendation.platform} ({recommendation.format})"):
                        st.markdown(f"**🕒 Best Time to Post:** {recommendation.best_time}")
                        st.markdown(f"**🎣 Hook:**")
                        st.info(recommendation.hook)
                        st.markdown(f"**✍️ Description:**")
                        st.write(recommendation.description)

async def render_competitor_analysis_page():
    """Renders the page for competitor analysis."""
    st.title("📊 Competitor Analysis")
    st.markdown("Enter a list of competitor social media usernames (one per line) to see their recent activity. Note: This feature currently uses mock data.")

    competitors_input = st.text_area("Competitor Usernames", "@garyvee\n@neilpatel\n@mkbhd", height=150, help="Enter one username per line.")

    if st.button("Analyze Competitors"):
        competitor_list = [c.strip() for c in competitors_input.split('\n') if c.strip() and c.startswith('@')]
        if not competitor_list:
            st.warning("Please enter at least one competitor username, starting with '@'.")
            return

        with st.spinner("🕵️‍♀️ Analyzing competitor data..."):
            competitor_data = await fetch_competitor_data(competitor_list)

        if not competitor_data:
            st.error("😔 Could not fetch competitor data.")
            return

        st.success(f"✅ Analysis complete for {len(competitor_list)} competitors.")

        # Group data by username
        data_by_competitor = {}
        for item in competitor_data:
            username_key = item.get('username', 'Unknown')
            if username_key not in data_by_competitor:
                data_by_competitor[username_key] = []
            data_by_competitor[username_key].append(item)

        # Create tabs for each competitor
        tab_list = st.tabs(list(data_by_competitor.keys()))

        for i, (username, data) in enumerate(data_by_competitor.items()):
            with tab_list[i]:
                st.subheader(f"Analysis for {username}")

                # Display data for each platform (Instagram, TikTok)
                for profile in data:
                    st.markdown(f"#### {profile.get('platform', 'N/A')}")
                    col1, col2 = st.columns(2)
                    col1.metric("Followers", f"{profile.get('follower_count', 0):,}")
                    col2.metric("Avg. Engagement", f"{profile.get('avg_engagement', 0.0)}%")

                    st.markdown("**Top Topics:**")
                    st.write(", ".join(profile.get('top_topics', [])))

                    st.markdown("**Recent Posts:**")
                    if profile.get('recent_posts'):
                        posts_df = pd.DataFrame(profile['recent_posts'])
                        posts_df['posted_at'] = pd.to_datetime(posts_df['posted_at']).dt.strftime('%Y-%m-%d')
                        st.dataframe(posts_df[['content', 'engagement', 'format', 'posted_at']], use_container_width=True)
                    else:
                        st.info("No recent posts found.")


# --- Main Application ---

async def main():
    """Main function to run the Streamlit app."""
    st.sidebar.title("Navigation")

    page_options = {
        "Home": render_home_page,
        "Trend Dashboard": render_trend_dashboard,
        "AI Content Strategy": render_ai_strategy_page,
        "Competitor Analysis": render_competitor_analysis_page,
    }

    selected_page = st.sidebar.radio("Choose a tool", list(page_options.keys()))

    # Render the selected page
    page_func = page_options[selected_page]
    if asyncio.iscoroutinefunction(page_func):
        await page_func()
    else:
        page_func()

    # Add a cache clearing button to the sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("Cache is cleared automatically every 15 minutes.")
    if st.sidebar.button("Clear Cache Now"):
        clear_trends_cache()
        st.sidebar.success("Data cache has been cleared!")
        st.rerun()

if __name__ == "__main__":
    # This is a common pattern to run async functions in Streamlit
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the async main function
    loop.run_until_complete(main())
