from django.urls import path , include  # type: ignore
from .views import * 

urlpatterns = [

    #Authentification

    path("register/",Register_Page,name="register_page"),
    path("login/",Login_Page,name="login_page"),
    path("login_action/",login_action,name="login_action"),
    path('logout/',log_out,name="logout"),

    #Les routes pour les templates 

    path("homepage/",homepage,name="homepage"),
    path("dashboardpage/",DashboardPage,name="dashboardpage"),
    path("profile/",Profile_Page,name="profile"),
    path('create_ao/',create_ao,name="create_ao"),
    path('evolution/',evolution,name="evolution"),
    path('evolution2/',evolution2,name="evolution2"),
    path('evolution3/',evolution3,name="evolution3"),
    path('display_AV_project/',display_AV_project,name="display_AV_project"),
    path('membres/',membres,name="membres"),
    


    #User 
    path("supprimer_user/<int:user_id>",supprimer_user,name="supprimer_user_dahsboard"),
    path('supprimer_own_profile/',supprimer_own_profile,name="supprimer_own_profile"),
    path("modify_password/",changer_mot_de_passe,name="modifypassword"),
    path("modify_personnal_info",modifier_profil,name="modifier_profil"),
    path('confirmer_new_user/<int:user_id>',Confirmer_New_User,name="Confirmer_New_User"),
    path('Other_profile/<int:user_id>',Visualiser_Other,name="Visualiser_Other"),
    path('edit_profile_page/<int:user_id>',Edit_Profile,name="Edit_Profile"),
    path('edit_user/<int:user_id>',edit_user,name="edit_user"),

    
    #Chatbot
    path('chat/', chat_view, name='chat'),

    
    #Graphe
    path('api/charts/gagnee/', api_chart_gagnee, name='api_chart_gagnee'),
    path('api/charts/refusee/', api_chart_refusee, name='api_chart_refusee'),
    path('api/charts/comparatif/',api_chart_comparatif, name='api_chart_comparatif'),


    #Project
    path('delete_project/<int:project_id>',delete_project,name="deleteproject"),
    path('delete_project2/<int:project_id>',delete_project2,name="deleteproject2"),
    path('create_project/',create_project,name="create_project"),
    path('get_project/',Get_main_project,name="Get_main_project"),
    path('Get_AV_project/',Get_AV_project,name="Get_AV_project"),
    path('specific_project/<int:project_id>',Get_specific_project,name="Get_specific_project"),
    path('modifier_project_page/<int:project_id>',modifier_project_page,name="modifier_project_page"),
    path('edit_project/<int:project_id>',edit_project,name="edit_project"),
    path('imp/<int:projet_id>',Imprimerie,name="Imprimerie"),
    path('dowload_pdf/<int:project_id>',download_project_pdf,name="download_project_pdf"),

    #Réclamation
    path('réclamation/',reclamation_page,name="reclamation_page"),
    path('gestion_reclamation/',Gestion_Reclamation,name="Gestion_Reclamation"),
    path('confirmer_reclamation/<int:id>',Passer_En_Cours,name="Passer_En_Cours"),
    path('Accept_reclamation/<int:id>',Accept_Reclamation,name="Accept_Reclamation"),
    path('Refuse_reclamation/<int:id>',Refuse_Reclamation,name="Refuse_Reclamation"),
    path('Reclamation_creation/',create_reclamation,name="create_reclamation"),

    #Logs
    path('logs/',Logs_Page,name="Logs_Page"),

    #Client
    path('Gestion_client/',Client_Page,name="Client_Page"),
    path('créer_client/',Créer_Client,name="Créer_Client"),
    path('supprimer_client/<int:client_id>',Supprimer_Client,name="Supprimer_Client"),
    path('edit_client/<int:client_id>',edit_client,name="edit_client"),
    path('edit_client_action/<int:client_id>',edit_client_action,name="edit_client_action"),

    #NEW
    path('new_user/',ajouter_new_user_page,name="ajouter_new_user_page"),
    path("create_user/", create_user, name="create_user_action"),
    path('api2/charts/gagnee/', api_chart_gagnee2, name='api_chart_gagnee2'),
    path('api3/charts/gagnee/', api_chart_gagnee3, name='api_chart_gagnee3'),
    path('api2/charts/refusee/', api_chart_refusee2, name='api_chart_refusee2'),
    path('api2/charts/comparatif/',api_chart_comparatif2, name='api_chart_comparatif2'),
    path('evolution2_page/',evolution2_Page,name="evolution2_Page"),
    path('evolution_PS/',evolutionPS_page,name="evolutionPS_page"),
    path('evolution_PEC/',evolitionPEC_page,name="evolitionPEC_page"),
    path('evolution_PAS/',evolitionPAS_page,name="evolitionPAS_page"),
]
