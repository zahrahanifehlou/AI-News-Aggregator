from datetime import datetime


class NewsletterBuilder:

    def build_text(self, articles):

        date = datetime.utcnow().strftime("%Y-%m-%d")

        content = []
        content.append(f"DAILY AI NEWS DIGEST - {date}\n")
        content.append("=" * 60)

        for i, article in enumerate(articles, 1):

            content.append(f"\n{i}. {article.title} (Score: {article.score})")
            content.append(f"Source: {article.source}")
            content.append(f"Categories: {', '.join(article.categories or [])}\n")

            content.append("Summary:")
            content.append(article.summary)
            content.append("-" * 60)

        return "\n".join(content)



    def build_html(self, articles):

        html = """
        <html>
        <body>
        <h1>Daily AI News Digest</h1>
        """

        for article in articles:

            html += f"""
            <hr>
            <h2>{article.title}</h2>
            <p><b>Score:</b> {article.score}</p>
            <p><b>Categories:</b> {', '.join(article.categories or [])}</p>
            <pre>{article.summary}</pre>
            """

        html += "</body></html>"

        return html