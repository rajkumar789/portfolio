from portfolio.models import Project, Article, Certification

def get_dynamic_context():
    """Fetches and formats dynamic content from the database for the AI context."""
    context_parts = []

    # 1. Projects
    projects = Project.objects.all()
    if projects.exists():
        context_parts.append("Here are Raj's Projects:")
        for p in projects:
            context_parts.append(f"- {p.title}: {p.description} (Tech: {p.technologies})")
    
    # 2. Articles
    articles = Article.objects.all()
    if articles.exists():
        context_parts.append("\nHere are Raj's Articles:")
        for a in articles:
            context_parts.append(f"- {a.title}: {a.summary}")

    # Certifications
    certs = Certification.objects.all().order_by('-issue_date')
    if certs.exists():
        context_parts.append("\nCERTIFICATIONS:")
        for c in certs:
            context_parts.append(f"- {c.title} from {c.issuer} ({c.issue_date})")

    return "\n".join(context_parts)
