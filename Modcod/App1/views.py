from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from .models import CustomUser , Project , Reclamation , Logs , Client
from .forms import CustomUserCreationForm
from django.http import HttpResponse , Http404, HttpResponseRedirect # type: ignore
from django.contrib.auth import login , authenticate , logout  # type: ignore
from django.contrib.auth.decorators import login_required # type: ignor
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from .chatbot import get_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.db.models.functions import TruncMonth , ExtractYear
from collections import defaultdict
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseBadRequest
from datetime import datetime
from django.template.loader import get_template , TemplateDoesNotExist
from xhtml2pdf import pisa # type: ignore
import random
from django.template.loader import render_to_string
from weasyprint import HTML # type: ignore
from django.utils.timesince import timesince
from django.utils.timezone import now


#Authentification
def Register_Page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Inscription réussie. Connectez-vous maintenant.")
                return redirect('login_page')
            except Exception as e:
                error_msg = f"Erreur lors de l'enregistrement : {str(e)}"
                messages.error(request, error_msg)
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"{error}")
                    else:
                        error_messages.append(f"{field.capitalize()}: {error}")
            messages.error(request, " | ".join(error_messages))
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
def Login_Page(request):
    return render(request,"auth/login.html")
def login_action(request):
    if request.method != "POST":
        messages.error(request, "Méthode non autorisée.")
        return redirect('login')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        messages.error(request, "Veuillez remplir tous les champs.")
        return redirect('login_page')
    try:
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('login_page')
        if user.role == "Utilisateur_Temporaire":
            messages.error(request, "Impossible de se connecter, votre compte est en cours de vérification par un admin. Merci d'avance.")
            return redirect('login_page')
        login(request, user)
        messages.success(request, "Connexion avec succès.")
        return redirect('homepage')
    except Exception as e:
        messages.error(request, f"Erreur lors de la connexion : {str(e)}")
        return redirect('login_page')
@login_required(login_url="/modcod/login")
def log_out(request):
    logout(request)
    messages.success(request,"Déconnexion avec succés!")
    return redirect('login_page')

#Templates
@login_required(login_url="/modcod/login")
def homepage(request):
    return render(request, "pages/main.html",{'main':'TA'})
@login_required(login_url="/modcod/login")
def DashboardPage(request):
    Users = CustomUser.objects.all()
    Projects = Project.objects.all()
    count = {
        "user" : CustomUser.objects.all().count() , 
        "project_gagnée" : Project.objects.filter(status = "PG").count() , 
        "project_refusée" : Project.objects.filter(status = "PP").count() ,
        "Project_avant_vente" : Project.objects.filter(status = "PA").count(),
        "Project_En_Cours" : Project.objects.filter(status = "PEC").count(),
    }
    etat_data = Project.objects.values('status').annotate(total=Count('status'))
    total = sum(item['total'] for item in etat_data) or 1  
    labels = [item['status'] for item in etat_data]
    data = [round((item['total'] / total) * 100, 2) for item in etat_data]
    context = {
        "etat_labels": labels,
        "etat_percentages": data,
    }
    return render(request,"admin/dashboard.html",{'users' : Users , 'projects' : Projects , "count" : count , "context":context})
@login_required(login_url="/modcod/login")
def Profile_Page(request):
    return render(request,"private/profile.html")
@login_required(login_url="/modcod/login")
def create_ao(request):
    clients = Client.objects.all()
    return render(request,"pages/create_ao.html",{'clients' : clients,"main":"create"})
@login_required(login_url="/modcod/login")
def evolution(request):
    return render(request,"data/evolution.html")
@login_required(login_url="/modcod/login")
def evolution2(request):
    return render(request,"data/evolution2.html")
@login_required(login_url="/modcod/login")
def evolution3(request):
    return render(request,"data/evolution3.html")
@login_required(login_url="/modcod/login")
def display_AV_project(request):
    return render(request,"pages/Av_display.html",{'main':'AV'})
def test(request):
    return render(request,"it/test.html")
@login_required(login_url="/modcod/login")
def Get_main_project(request):
    projects = Project.objects.exclude(status="PA").order_by('-date_creation')
    data = list(projects.values(
        'id', 'reference', 'reference_modcod', 'objet', 'date_limite_reponse',
        'prospectus', 'editeur', 'documents_manquants', 'contexte', 'etat_d_avancement','status'
    ))
    editeurs_uniques = list(
        Project.objects.exclude(editeur__isnull=True)
        .exclude(editeur__exact='')
        .values_list('editeur', flat=True)
        .distinct()
    )
    return JsonResponse({'projects': data, 'editeurs': editeurs_uniques})
@login_required(login_url="/modcod/login")
def Get_AV_project(request):
    projects = Project.objects.filter(status="PA").order_by('-date_creation')
    data = list(projects.values(
        'id', 'reference', 'reference_modcod', 'objet', 'date_limite_reponse',
        'prospectus', 'editeur', 'documents_manquants', 'contexte', 'etat_d_avancement','status'
    ))
    editeurs_uniques = list(
        Project.objects.exclude(editeur__isnull=True)
        .exclude(editeur__exact='')
        .values_list('editeur', flat=True)
        .distinct()
    )
    return JsonResponse({'projects': data, 'editeurs': editeurs_uniques})
@login_required(login_url="/modcod/login")
def Get_specific_project(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        project.montant_caution = f"{float(project.montant_caution):,.2f}".replace(",", " ").replace(".", ",")
        project.estimation_projet = f"{float(project.estimation_projet):,.2f}".replace(",", " ").replace(".", ",")
        return render(request, "it/specific_project.html", {"project": project})
    except Exception as e:
        messages.error(request,f"Une erreur inattendue est survenue, veuillez réessayer plus tard {str(e)} ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url="/modcod/login")
def membres(request):
    try:
        users = CustomUser.objects.all()
        return render(request, 'pages/membres.html', {'users': users , 'main':'membre'})
    except CustomUser.DoesNotExist:
        return render(request, 'pages/membres.html', {'users': []})
    except Exception as e:
        messages.error(f"Une erreur s'est produite lors du chargement des membres détails : {str(e)} ")
        return redirect('homepage')

#User 
@login_required(login_url="/modcod/login")
def supprimer_user(request, user_id):
    if  not request.user.is_staff:
        messages.error(request, "Vous n'avez pas la permission de supprimer un utilisateur.")
        raise PermissionDenied("Accès interdit.")
    try:
        user = CustomUser.objects.get(id=user_id)
        if user == request.user:
            messages.warning(request, "Vous ne pouvez pas supprimer votre propre compte.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if user.is_superuser:
            messages.error(request, "Impossible de supprimer un superutilisateur.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        user.delete()
        messages.success(request, f"Suppression de l'utilisateur ID {user_id} réussie.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
    except DatabaseError as e:
        messages.error(request, f"Erreur base de données : {str(e)}")
    except Exception as e:
        messages.error(request, f"Erreur inattendue : {str(e)}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url="/modcod/login")
def supprimer_own_profile(request):
    try:
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Suppression de votre compte avec succès.")
        return redirect('login_page')
    except ObjectDoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('login_page')
    except DatabaseError as e:
        messages.error(request, f"Erreur de base de données : {str(e)}")
        return redirect('login_page')
    except Exception as e:
        messages.error(request, f"Une erreur inattendue s'est produite : {str(e)}")
        return redirect('login_page')
@login_required(login_url='/modcod/login')
def changer_mot_de_passe(request):
    if request.method == "POST":
        current_password = request.POST.get("currentPassword")
        new_password = request.POST.get("newPassword")
        confirm_password = request.POST.get("confirmPassword")
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Mot de passe actuel incorrect.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if user.check_password(new_password):
            messages.error(request,"Veuillez saisir un nouveau mot de passe différent à celui actuel")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if new_password != confirm_password:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        try:
            validate_password(new_password, user=user)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Mot de passe mis à jour avec succès.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'private/profile.html')
@login_required(login_url='/modcod/login')
def modifier_profil(request):
    if request.method == "POST":
        user = request.user
        try:
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            address = request.POST.get("adress", "").strip()
            if CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
                messages.error(request, "Cet email est déjà utilisé par un autre compte.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.adress = address
            user.full_clean()  
            user.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)
        except IntegrityError:
            messages.error(request, "Erreur d'intégrité : données dupliquées ou invalides.")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'private/profile.html')
@login_required(login_url="/modcod/login")
def Confirmer_New_User(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour effectuer cette action.")
        return redirect('login')
    if not request.user.is_staff:
        raise PermissionDenied("Vous n'avez pas la permission de confirmer des utilisateurs.")
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        if user.role == 'Utilisateur_Confirmé':
            messages.info(request, f"L'utilisateur d'ID {user.id} est déjà confirmé.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        user.role = 'Utilisateur_Confirmé'
        user.save()
        messages.success(request, f"L'utilisateur d'ID {user.id} a été confirmé avec succès.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except ObjectDoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('user_list')  
    except ValidationError as ve:
        messages.error(request, f"Erreur de validation : {ve}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except IntegrityError:
        messages.error(request, "Erreur d'intégrité de la base de données.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except DatabaseError:
        messages.error(request, "Une erreur est survenue lors de l'accès à la base de données.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        messages.error(request, f"Erreur inattendue : {str(e)}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url='/modcod/login')
def Visualiser_Other(request,user_id):
    user = get_object_or_404(CustomUser , id = user_id)
    return render(request,'private/profile2.html',{'user' : user })
@login_required(login_url='/modcod/login')
def Edit_Profile(request,user_id):
    try : 
        user = get_object_or_404(CustomUser , id = user_id)
        return render(request,'pages/modifier_profil.html',{'user' : user})
    except CustomUser.DoesNotExist :
        messages.error(request,f"Le user d'id {user_id} n'est pas trouvé ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
@login_required
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        phone_number = request.POST.get('phoneNumber', '').strip()
        role = request.POST.get('role', '').strip()
        address = request.POST.get('address', '').strip()
        if username != user_to_edit.username and CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if email != user_to_edit.email and CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, "Cette adresse email est déjà utilisée.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        user_to_edit.username = username
        user_to_edit.email = email
        user_to_edit.first_name = first_name
        user_to_edit.last_name = last_name
        user_to_edit.phone_number = phone_number 
        user_to_edit.role = role                    
        user_to_edit.adress = address              
        user_to_edit.save()
        messages.success(request, "Utilisateur mis à jour avec succès.")
        return redirect('dashboardpage')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#Chatbot
@csrf_exempt
@require_http_methods(["POST"])
def chat_view(request):
    user_message = request.POST.get('message', '')
    bot_response = get_response(user_message)
    return JsonResponse({'response': bot_response})


#Graphe
@login_required(login_url="/modcod/login")
def api_chart_gagnee(request):
    projets = Project.objects.filter(status="PG").annotate(
        month=TruncMonth('date_limite_reponse'),
        year=ExtractYear('date_limite_reponse')
    )
    data = projets.values('month').annotate(count=Count('id')).order_by('month')
    overall_labels = [item['month'].strftime("%b %Y") for item in data]
    overall_values = [item['count'] for item in data]
    years_data = defaultdict(lambda: { 'labels': [], 'values': [] })
    temp_year_month_counts = defaultdict(lambda: defaultdict(int))
    for proj in projets:
        m = proj.month
        y = proj.year
        temp_year_month_counts[y][m] += 1
    for year, months_dict in temp_year_month_counts.items():
        labels = []
        values = []
        from datetime import datetime
        import calendar
        for month_num in range(1, 13):
            dt = datetime(year, month_num, 1)
            label = dt.strftime("%b %Y")
            labels.append(label)
            count = 0
            for m_date, c in months_dict.items():
                if m_date.year == year and m_date.month == month_num:
                    count = c
                    break
            values.append(count)
        years_data[str(year)] = {
            "labels": labels,
            "values": values
        }
    response = {
        "overall": {
            "labels": overall_labels,
            "values": overall_values
        },
        "years": dict(years_data)
    }
    return JsonResponse(response)
@login_required(login_url="/modcod/login")
def api_chart_refusee(request):
    projets = Project.objects.filter(status="PP").annotate(
        month=TruncMonth('date_limite_reponse'),
        year=ExtractYear('date_limite_reponse')
    )
    data = projets.values('month').annotate(count=Count('id')).order_by('month')
    overall_labels = [item['month'].strftime("%b %Y") for item in data]
    overall_values = [item['count'] for item in data]
    years_data = defaultdict(lambda: { 'labels': [], 'values': [] })
    temp_year_month_counts = defaultdict(lambda: defaultdict(int))
    for proj in projets:
        m = proj.month
        y = proj.year
        temp_year_month_counts[y][m] += 1
    for year, months_dict in temp_year_month_counts.items():
        labels = []
        values = []
        import calendar
        for month_num in range(1, 13):
            dt = datetime(year, month_num, 1)
            label = dt.strftime("%b %Y")
            labels.append(label)
            count = 0
            for m_date, c in months_dict.items():
                if m_date.year == year and m_date.month == month_num:
                    count = c
                    break
            values.append(count)
        years_data[str(year)] = {
            "labels": labels,
            "values": values
        }
    response = {
        "overall": {
            "labels": overall_labels,
            "values": overall_values
        },
        "years": dict(years_data)
    }
    return JsonResponse(response)
@login_required(login_url="/modcod/login")
def api_chart_comparatif(request):
    projets_gagnee = Project.objects.filter(status="PG").annotate(
        month=TruncMonth('date_limite_reponse'),
        year=ExtractYear('date_limite_reponse')
    )
    projets_refusee = Project.objects.filter(status="PP").annotate(
        month=TruncMonth('date_limite_reponse'),
        year=ExtractYear('date_limite_reponse')
    )
    def build_year_month_counts(projets):
        counts = defaultdict(lambda: defaultdict(int))
        for p in projets:
            counts[p.year][p.month] += 1
        return counts
    gagnee_counts = build_year_month_counts(projets_gagnee)
    refusee_counts = build_year_month_counts(projets_refusee)
    all_years = set(list(gagnee_counts.keys()) + list(refusee_counts.keys()))
    all_months = set()
    for y in all_years:
        all_months.update(gagnee_counts[y].keys())
        all_months.update(refusee_counts[y].keys())
    all_months = sorted(all_months)

    overall_labels = [dt.strftime("%b %Y") for dt in all_months]
    overall_gagnee = []
    overall_refusee = []
    for month_dt in all_months:
        total_gagnee = 0
        total_refusee = 0
        for y in all_years:
            total_gagnee += gagnee_counts[y].get(month_dt, 0)
            total_refusee += refusee_counts[y].get(month_dt, 0)
        overall_gagnee.append(total_gagnee)
        overall_refusee.append(total_refusee)
    years_data = {}
    for y in all_years:
        labels = []
        gagnee_values = []
        refusee_values = []
        for month_num in range(1, 13):
            dt = datetime(y, month_num, 1)
            labels.append(dt.strftime("%b %Y"))
            gagnee_values.append(gagnee_counts[y].get(dt, 0))
            refusee_values.append(refusee_counts[y].get(dt, 0))
        years_data[str(y)] = {
            "labels": labels,
            "gagnee": gagnee_values,
            "refusee": refusee_values,
        }

    response = {
        "overall": {
            "labels": overall_labels,
            "gagnee": overall_gagnee,
            "refusee": overall_refusee,
        },
        "years": years_data,
        "available_years": sorted([str(y) for y in all_years])
    }
    return JsonResponse(response)


#Project 
@login_required(login_url="/modcod/login")
def delete_project(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        messages.success(request, f"Suppression de l'appel d'offre n°{project_id} effectuée avec succès.")
    except Project.DoesNotExist:
        messages.error(request, f"Le projet avec l'ID {project_id} n'existe pas.")
    except Exception as e:
        messages.error(request, "Une erreur inattendue est survenue lors de la suppression.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url="/modcod/login")
def delete_project2(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        messages.success(request, f"Suppression de l'appel d'offre n°{project_id} effectuée avec succès.")
    except Project.DoesNotExist:
        messages.error(request, f"Le projet avec l'ID {project_id} n'existe pas.")
    except Exception as e:
        messages.error(request, "Une erreur inattendue est survenue lors de la suppression.")
    return redirect('homepage')
@login_required(login_url='/modcod/login')
def create_project(request):
    if request.method == 'POST':
        try:
            reference = request.POST.get('reference', '').strip()
            reference_modcod = request.POST.get('reference_modcod', '').strip()
            objet = request.POST.get('object', '').strip()
            date_limite = request.POST.get('date_limite')
            client = request.POST.get('client','')
            try:
                c = get_object_or_404(Client, username=client)
            except Http404:
                messages.success(request,"Le client que vous avez saisi n'existe pas dans la base de donnée merci de l'ajouter au niveau du dashboard")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            caution = request.POST.get('caution','ELECTRONIQUE')
            montant_caution = request.POST.get('montant_caution','0.00')
            estimation_projet = request.POST.get('estimation_projet','0.00')
            delai_execution = request.POST.get('date_execution')
            prospectus = request.POST.get('prospectus')
            editeur = request.POST.get('editeur', '').strip()
            etat_d_avancement = request.POST.get('etat_d_avancement','').strip()
            etape_suivante = request.POST.get('etape_suivant', '').strip()
            contexte = request.POST.get('contexte', '').strip()
            documents_manquants = request.POST.get('documents_manquants', '').strip()
            status = request.POST.get('status','PA')
            if not reference or not reference_modcod or not objet or not date_limite:
                messages.warning(request, "Les champs Référence, Référence ModCod, Objet et Date Limite sont obligatoires.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            Project.objects.create(
                reference=reference,
                client = c , 
                reference_modcod=reference_modcod,
                objet=objet,
                date_limite_reponse=parse_datetime(date_limite),
                caution=caution,
                montant_caution = montant_caution , 
                estimation_projet = estimation_projet , 
                delai_execution=delai_execution if delai_execution else None,
                prospectus=prospectus if prospectus else None,
                editeur=editeur,
                contexte=contexte,
                documents_manquants=documents_manquants,
                etat_d_avancement=etat_d_avancement,
                etape_suivante=etape_suivante,
                status  = status , 
            )
            messages.success(request, "✅ Projet créé avec succès !")
            return redirect('homepage')  

        except ValueError as ve:
            messages.error(request, f"Erreur de format dans les champs (date ou texte). Détail : {ve}")
        except DatabaseError as db_err:
            messages.error(request, "Erreur de base de données. Veuillez réessayer.")
        except Exception as e:
            messages.error(request, f"Une erreur inattendue est survenue. Détail : {e}")

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'App1/create_project.html')
@login_required(login_url="/modcod/login")
def modifier_project_page(request, project_id):
    try:
        if not isinstance(project_id, int):
            return HttpResponseBadRequest("ID de projet invalide.")
        project = get_object_or_404(Project, id=project_id)
        clients = Client.objects.all()
        return render(request, "pages/modifier_Ao.html", {'project': project , 'clients' : clients})
    except Project.DoesNotExist as e :
        return messages.error(e)
    except ValueError as e:
        messages.error(request,"Erreur de valeur détectée.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        messages.error(request,'Une erreur inattendue est survenue.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url="/modcod/login")
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.reference = request.POST.get('reference', '')
        project.reference_modcod = request.POST.get('reference_modcod', '')
        project.objet = request.POST.get('objet', '')
        client = request.POST.get('client','')
        project.montant_caution = request.POST.get('montant_caution')
        project.estimation_projet = request.POST.get('estimation_projet')
        try:
            c = get_object_or_404(Client, username=client)
            project.client = c 
        except Http404:
            messages.success(request,"Le client que vous avez saisi n'existe pas dans la base de donnée merci de l'ajouter au niveau du dashboard")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        date_limite_reponse = request.POST.get('date_limite_reponse')
        if date_limite_reponse:
            project.date_limite_reponse = date_limite_reponse
        project.caution = request.POST.get('caution', 'ELECTRONIQUE')
        delai_execution = request.POST.get('delai_execution')
        if delai_execution:
            project.delai_execution = delai_execution
        prospectus = request.POST.get('prospectus')
        if prospectus:
            project.prospectus = prospectus
        project.editeur = request.POST.get('editeur', '')
        project.contexte = request.POST.get('contexte', '')
        project.documents_manquants = request.POST.get('documents_manquants', '')
        project.etat_d_avancement = request.POST.get('etat_d_avancement', '')
        project.etape_suivante = request.POST.get('etape_suivante', '')
        project.status = request.POST.get('status','PA')
        project.save()
        messages.success(request,"Modification avec succés")
        return redirect('Get_specific_project',project.id) 
    return render(request, 'edit_project.html', {'project': project})

#PDF
def Imprimerie(request,projet_id):
    projet = get_object_or_404(Project,id = projet_id)
    valeur_str = str(projet.montant_caution)
    valeur_nettoyee = valeur_str.replace(" ", "").replace(",", ".")
    montant = float(valeur_nettoyee)
    projet.montant_caution = f"{montant:,.2f}".replace(",", " ").replace(".", ",")   
    valeur_str = str(projet.estimation_projet)  
    valeur_nettoyee = valeur_str.replace(" ", "").replace(",", ".")
    montant = float(valeur_nettoyee)
    projet.estimation_projet = f"{montant:,.2f}".replace(",", " ").replace(".", ",")  
    return render(request,'pages/PDF.html',{'projet':projet})
def download_project_pdf(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    valeur_str = str(project.montant_caution)
    valeur_nettoyee = valeur_str.replace(" ", "").replace(",", ".")
    montant = float(valeur_nettoyee)
    project.montant_caution = f"{montant:,.2f}".replace(",", " ").replace(".", ",")   
    valeur_str = str(project.estimation_projet)  
    valeur_nettoyee = valeur_str.replace(" ", "").replace(",", ".")
    montant = float(valeur_nettoyee)
    project.estimation_projet = f"{montant:,.2f}".replace(",", " ").replace(".", ",")  
    html_string = render_to_string('pages/PDF2.html', {'projet': project})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="project_{project.id}.pdf"'
    return response

#Réclamation
def reclamation_page(request):
    return render(request,"pages/reclamation.html")
@login_required(login_url='/modcod/login')
def Gestion_Reclamation(request):
    reclamations = Reclamation.objects.all().order_by("-date_creation")
    urgent = Reclamation.objects.filter(priorité = "Urgent").count()
    faible = Reclamation.objects.filter(priorité = "Faible").count()
    moyen = Reclamation.objects.filter(priorité = "Moyen").count()
    return render(request, 'private/gestion_reclamation.html', {'reclamations': reclamations , 'urgent' : urgent , 'moyen' : moyen , 'faible' : faible})
@login_required(login_url='/modcod/login')
def Passer_En_Cours(request, id):
    try:
        reclamation = Reclamation.objects.get(id=id)
        if reclamation.status == "En cours":
            messages.info(request, f"La réclamation d'ID {reclamation.id} est déjà en cours.")
        else:
            reclamation.status = "En cours"
            reclamation.save()
            messages.success(request, f"La réclamation d'ID {reclamation.id} est passée à l'étape suivante : En cours ✅")
    except ValueError:
        messages.error(request, "ID invalide fourni. ⚠️")
    except ObjectDoesNotExist:
        messages.error(request, f"Aucune réclamation trouvée avec l'ID {id}. ❌")
    except ValidationError as e:
        messages.error(request, "Erreur de validation lors de la mise à jour de la réclamation. 🚫")
    except Exception as e:
        messages.error(request, "Une erreur inattendue s'est produite. Veuillez réessayer plus tard. 🛑")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url='/modcod/login')
def Accept_Reclamation(request, id):
    try:
        reclamation = Reclamation.objects.get(id=id)
        if reclamation.status == "Résolu":
            messages.info(request, f"La réclamation d'ID {reclamation.id} est déjà marquée comme résolue. ✅")
        else:
            reclamation.status = "Résolu"
            reclamation.save()
            messages.success(request, f"La réclamation d'ID {reclamation.id} a été résolue avec succès. 🟢")
    except ValueError:
        messages.error(request, "ID invalide fourni. ⚠️")
    except ObjectDoesNotExist:
        messages.error(request, f"Aucune réclamation trouvée avec l'ID {id}. ❌")
    except ValidationError as e:
        messages.error(request, "Erreur de validation lors de la mise à jour. 🚫")
    except Exception as e:
        messages.error(request, "Une erreur inattendue s'est produite. 🛑")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required(login_url='/modcod/login')
def Refuse_Reclamation(request, id):
    try:
        reclamation = Reclamation.objects.get(id=id)
        if reclamation.status == "Non résolu":
            messages.info(request, f"La réclamation d'ID {reclamation.id} est déjà marquée comme non résolue. ❎")
        else:
            reclamation.status = "Non résolu"
            reclamation.save()
            messages.success(request, f"La réclamation d'ID {reclamation.id} a été refusée. 🔴")
    except ValueError:
        messages.error(request, "ID invalide fourni. ⚠️")
    except ObjectDoesNotExist:
        messages.error(request, f"Aucune réclamation trouvée avec l'ID {id}. ❌")
    except ValidationError as e:
        messages.error(request, "Erreur de validation lors de la mise à jour. 🚫")
    except Exception as e:
        messages.error(request, "Une erreur inattendue s'est produite. 🛑")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def create_reclamation(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username", "")
            email = request.POST.get("email", "")
            reference = request.POST.get("reference", "")
            category = request.POST.get("category", "Autre")
            priority = request.POST.get("priority", "Not defined")
            subject = request.POST.get("subject", "")
            description = request.POST.get("description", "")
            piece = request.FILES.get("attachments")  
            if not username or not email or not category or not subject or not description:
                messages.error(request, "Veuillez remplir tous les champs obligatoires marqués par *.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            reclamation = Reclamation.objects.create(
                username=username,
                email=email,
                référence=reference,
                catégorie=category,
                priorité=priority,
                sujet=subject,
                description=description,
                piece=piece
            )
            messages.success(request, f"Réclamation envoyée avec succès ! Numéro de suivi : #{reclamation.id} ✅")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            messages.error(request, "Une erreur est survenue lors de l'envoi de la réclamation. Veuillez réessayer. ❌")
            print(f"[ERREUR création réclamation] {e}") 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "reclamations/formulaire_reclamation.html")


#Logs
@login_required(login_url='/modcod/login')
def Logs_Page(request):
    logs = Logs.objects.select_related('user').all().order_by('-date_creation')
    for log in logs:
        log.elapsed_time = timesince(log.date_creation, now()) + " ago"
    return render(request, 'private/logs.html', {'logs': logs})


#Client
@login_required(login_url="/modcod/login")
def Client_Page(request):
    clients = Client.objects.all()
    total = Client.objects.count()
    return render(request,'pages/client.html',{'total':total , 'clients':clients })
@login_required(login_url="/modcod/login")
def Créer_Client(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            Client.objects.get(username=username)
            messages.error(request, f"Le client '{username}' existe déjà dans la base de données.")
        except Client.DoesNotExist:
            Client.objects.create(username=username)
            messages.success(request, f"Le client '{username}' a été enregistré avec succès.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def Supprimer_Client(request,client_id):
    try : 
        client = get_object_or_404(Client , id = client_id )
        client.delete()
        messages.success(request,f"Suppression du client {client.username} avec succés")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Client.DoesNotExist :
        messages.error(request,f"Le clinet d'id {client_id} n'existe pas")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def edit_client(request,client_id):
    try : 
        client = get_object_or_404(Client , id = client_id )
        return render(request,'pages/edit_client.html',{'client':client})
    except Client.DoesNotExist :
        messages.error(request,f"Le clinet d'id {client_id} n'existe pas")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def edit_client_action(request, client_id):
    if request.method == "POST":
        try:
            client = get_object_or_404(Client, id=client_id)
            username = request.POST.get('username', '').strip()
            if Client.objects.filter(username=username).exclude(id=client.id).exists():
                messages.error(request, f"Le client '{username}' existe déjà dans la base de données.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            client.username = username
            client.save()
            messages.success(request, "Changement de username effectué avec succès.")
            return redirect("Client_Page")
        except Client.DoesNotExist:
            messages.error(request, f"Le client avec l'ID {client_id} n'existe pas.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))