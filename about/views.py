from django.views.generic import TemplateView

import frontmatter


class MarkdownView(TemplateView):
    template_name = "markdown_base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = frontmatter.load(f"markdown/{self.markdown_name}")
        markdown_content = post.content
        meta = post.metadata
        context["markdown_content"] = markdown_content
        context["frontmatter"] = meta
        return context


class AboutPageView(MarkdownView):
    markdown_name = "about.md"


class CopyrightPageView(MarkdownView):
    markdown_name = "copyright.md"


class OpenSourceLicensePageView(MarkdownView):
    markdown_name = "open_source.md"


class StyleGuidePageView(MarkdownView):
    markdown_name = "style_guide.md"
