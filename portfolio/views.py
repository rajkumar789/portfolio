import json
import os
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import default_storage
from django.utils.text import slugify
import google.generativeai as genai
from .models import Project, Article, Certification, Subscription, CaseStudy
from .utils.ai_context import get_dynamic_context
from .decorators import rate_limit

@csrf_exempt
def upload_file(request):
    if not request.user.is_staff:
         return JsonResponse({'error': {'message': 'Unauthorized'}}, status=403)
         
    print("DEBUG: Entered upload_file view")
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        name, ext = os.path.splitext(upload.name)
        file_path = f"uploads/{slugify(name)}{ext}"
        saved_path = default_storage.save(file_path, upload)
        url = default_storage.url(saved_path)
        return JsonResponse({'url': url})
    return JsonResponse({'error': {'message': 'Upload failed'}})

# ... existing code ...

# ... existing get_cv_data function ...
# ... existing home, project_list, blog_list, certification_list, privacy_policy views ...

def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('images'), slug=slug)
    
    # Track unique visitors using session
    session_key = f'viewed_project_{project.id}'
    if not request.session.get(session_key, False):
        project.views += 1
        project.save(update_fields=['views'])
        request.session[session_key] = True
    
    # Check if liked
    is_liked = request.session.get(f'liked_project_{project.id}', False)

    return render(request, 'portfolio/project_detail.html', {'project': project, 'is_liked': is_liked})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'portfolio/blog_detail.html', {'blog': blog})




@rate_limit(limit=5, period=300) # 5 emails per 5 minutes
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            email = data.get('email', '')
            message = data.get('message', '')
            
            if not all([first_name, email, message]):
                return JsonResponse({'error': 'Please fill in all required fields'}, status=400)
            
            # Send email
            subject = f"Portfolio Contact: {first_name} {last_name}"
            email_message = f"""
New contact form submission:

From: {first_name} {last_name}
Email: {email}

Message:
{message}
            """
            
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,  # From email
                    ['rajsunar@rajsunar.live'],  # To email
                    fail_silently=False,
                )
            except Exception as email_error:
                print(f"Email sending error: {str(email_error)}")
                return JsonResponse({
                    'error': f'Failed to send email: {str(email_error)}. Please check your email settings.'
                }, status=500)
            
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Contact form error: {str(e)}")
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)



# Configure Gemini
import os
# WARNING: In production, use os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

PORTFOLIO_CONTEXT = """
You are an AI assistant for Raj Kumar Sunar's portfolio website.
Raj is a Detail-oriented Data Analyst based in West Sussex, UK.
Phone: +44 7949 514215, Email: rajkumarsoni280@gmail.com.

Education: Master of Science in Management with Data Analytics from BPP University (Sep 2023 - Sep 2024).

Technical Skills:
- Programming: Python, SQL.
- Visualization: Power BI, Tableau, Advanced Excel.
- Database: SQL, MySQL, MongoDB, PostgreSQL.
- Expertise: Machine Learning, Predictive Modelling, ETL Processes, Data Cleaning.

Experience:
- EduTech, Nepal (Feb 2023 - Sep 2023): Training Coordinator & IT Support. Led training needs assessments, managed CRM updates, provided IT support.

Projects:
1. Loan Data Automation System: Automated loan data processing, enhancing efficiency by 50%.
2. Machine Learning Model: Used ANN and Decision Tree for Customer Satisfaction prediction.
3. Full-Stack Portfolio: Built with Django.
4. Product Sales Analysis: Optimized sales methods using data visualization.

Certifications: Data Analyst Associate (DataCamp), Learning Data Analytics (LinkedIn), Visual Presentations (Visme).

Tone: Professional, concise, and helpful. Answer in the first person as if you are Raj's digital assistant.
"""

@rate_limit(limit=10, period=60) # 10 messages per minute
def chat_with_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Initialize Model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Get dynamic context
            dynamic_context = get_dynamic_context()
            full_context = f"{PORTFOLIO_CONTEXT}\n\nWEBSITE CONTENT:\n{dynamic_context}"
            
            # Create chat with history/context
            chat = model.start_chat(history=[
                {"role": "user", "parts": [full_context]},
                {"role": "model", "parts": ["Understood. I have been updated with the latest website content and am ready to answer questions about Raj Kumar Sunar."]}
            ])
            
            response = chat.send_message(user_message)
            
            return JsonResponse({'response': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)
            
            if Subscription.objects.filter(email=email).exists():
                return JsonResponse({'message': 'You are already subscribed!'})
            
            Subscription.objects.create(email=email)
            
            # Send Welcome Email
            from .utils.email import send_email
            subject = "Welcome to my Newsletter!"
            message = """
            Hi there,

            Thank you for subscribing to my newsletter!

            You'll now be the first to know when I publish new articles, projects, or earn new certifications.

            Best regards,
            Raj Kumar Sunar
            """
            try:
                send_email(email, subject, message)
            except Exception as e:
                print(f"Failed to send welcome email: {e}")
                # Don't fail the request if email fails, just log it

            return JsonResponse({'message': 'Successfully subscribed!'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@rate_limit(limit=10, period=60)
def summarize_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Accept both 'text' and 'content' for backward compatibility
            content = data.get('text') or data.get('content', '')
            content_type = data.get('type', 'content')
            
            if not content:
                return JsonResponse({'error': 'No content provided'}, status=400)

            # Initialize Model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"Please provide a concise summary (max 3 sentences) of the following {content_type}:\n\n{content}"
            
            response = model.generate_content(prompt)
            
            return JsonResponse({'summary': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
@ensure_csrf_cookie
def home(request):
    # Show only top 2 on home page
    projects = Project.objects.all().order_by('-created_at')[:4]
    articles = Article.objects.all().order_by('-date_posted')[:4]
    certifications = Certification.objects.all().order_by('-issue_date')[:4]
    case_studies = CaseStudy.objects.all().order_by('-date_posted')[:3]
    
    context = {
        'projects': projects,
        'articles': articles,
        'certifications': certifications,
        'case_studies': case_studies,
    }
    return render(request, 'portfolio/home.html', context)

def project_list(request):
    # Show ALL projects with pagination
    projects_list = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects_list, 6)  # Show 6 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(request, 'portfolio/project_list.html', {'projects': projects})

def article_list(request):
    # Show ALL articles with pagination
    articles_list = Article.objects.all().order_by('-date_posted')
    paginator = Paginator(articles_list, 6)  # Show 6 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portfolio/article_list.html', {'page_obj': page_obj})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    # Track unique visitors using session
    # Track unique visitors using session
    session_key = f'viewed_article_{article.id}'
    if not request.session.get(session_key, False):
        article.views += 1
        article.save(update_fields=['views'])
        request.session[session_key] = True
    
    # Check if liked
    is_liked = request.session.get(f'liked_article_{article.id}', False)
    
    return render(request, 'portfolio/article_detail.html', {'article': article, 'is_liked': is_liked})

def like_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content_type = data.get('type')
            content_id = data.get('id')
            
            if content_type == 'project':
                obj = get_object_or_404(Project, pk=content_id)
            elif content_type == 'article':
                obj = get_object_or_404(Article, pk=content_id)
            elif content_type == 'case_study':
                obj = get_object_or_404(CaseStudy, pk=content_id)
            else:
                return JsonResponse({'error': 'Invalid content type'}, status=400)
            
            # Use session to prevent multiple likes from same user
            session_key = f'liked_{content_type}_{content_id}'
            
            if not request.session.get(session_key, False):
                # User hasn't liked it yet -> Like
                obj.likes += 1
                obj.save(update_fields=['likes'])
                request.session[session_key] = True
                status = 'liked'
            else:
                # User already liked -> Unlike
                if obj.likes > 0:
                    obj.likes -= 1
                    obj.save(update_fields=['likes'])
                del request.session[session_key]
                status = 'unliked'
            
            return JsonResponse({'likes': obj.likes, 'status': status})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def certification_list(request):
    # Show ALL certifications with pagination
    certifications_list = Certification.objects.all().order_by('-issue_date')
    paginator = Paginator(certifications_list, 6)  # Show 6 certifications per page
    page_number = request.GET.get('page')
    certifications = paginator.get_page(page_number)
    return render(request, 'portfolio/certification_list.html', {'certifications': certifications})

def privacy_policy(request):
    return render(request, 'portfolio/privacy_policy.html')

def search(request):
    query = request.GET.get('q')
    projects = []
    articles = []
    
    if query:
        from django.db.models import Q
        projects = Project.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(technologies__icontains=query)
        ).distinct()
        
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    
    return render(request, 'portfolio/search_results.html', {
        'query': query,
        'projects': projects,
        'articles': articles
    })
# ... existing imports ...
from django.http import HttpResponse # Add this import at the top

# ... existing views ...

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://rajsunar.live/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def llms_txt(request):
    file_path = os.path.join(settings.BASE_DIR, 'portfolio', 'static', 'llms.txt')
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/plain")
    except FileNotFoundError:
        return HttpResponse("llms.txt not found.", status=404, content_type="text/plain")

def case_study_list(request):
    case_studies_list = CaseStudy.objects.all().order_by('-date_posted')
    paginator = Paginator(case_studies_list, 6)
    page_number = request.GET.get('page')
    case_studies = paginator.get_page(page_number)
    return render(request, 'portfolio/case_study_list.html', {'case_studies': case_studies})

def case_study_detail(request, slug):
    case_study = get_object_or_404(CaseStudy, slug=slug)
    
    # Track unique visitors using session
    session_key = f'viewed_casestudy_{case_study.id}'
    if not request.session.get(session_key, False):
        case_study.views += 1
        case_study.save(update_fields=['views'])
        request.session[session_key] = True
        
    # Check if liked
    is_liked = request.session.get(f'liked_case_study_{case_study.id}', False)
        
    return render(request, 'portfolio/case_study_detail.html', {'case_study': case_study, 'is_liked': is_liked})