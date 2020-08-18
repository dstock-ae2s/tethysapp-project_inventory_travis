from .model import Project, add_new_project, get_all_projects
from django.http import JsonResponse, HttpResponse, Http404
from .app import ProjectInventory as app

def get_project_list (request):
    if request.is_ajax() and request.method == 'POST':
        fac_id = request.POST['facility_id']

        project_list = get_all_projects()

        return_obj = {}
        fac_projname_list = []
        fac_projcost_list = []
        fac_projyear_list = []


        for project in project_list:
            if project.facility_id == fac_id:
                fac_projname_list.append(project.project)
                fac_projcost_list.append(project.cost)
                fac_projyear_list.append(project.planned_year)

        print(fac_projname_list)
        print(fac_projcost_list)
        print(fac_projyear_list)

        return_obj["project_name"] = fac_projname_list
        return_obj["cost"] = fac_projcost_list
        return_obj["planned_year"] = fac_projyear_list

        return JsonResponse(return_obj)


def save_updates_to_db (request):
#     if request.is_ajax() and request.method == 'POST':
#         fac_id = request.POST['facility_id']
#         project_name_list = request.POST['project_name_lis']
#         project_cost_list = request.POST['project_cost_list']
#         project_year_list = request.POST['project_year_list']
#         coordinates = request.POST['coordinates']
#
#         project_list = get_all_projects()
#
#         return_obj = {}
#         fac_projname_list = []
#         fac_projcost_list = []
#         fac_projyear_list = []
#
#
#         for project in project_list:
#             if project.facility_id == fac_id:
#                 fac_projname_list.append(project.project)
#                 fac_projcost_list.append(project.cost)
#                 fac_projyear_list.append(project.planned_year)
#
#         print(fac_projname_list)
#         print(fac_projcost_list)
#         print(fac_projyear_list)
#
#                 # num_existing_projects = fac_projname_list.len
#
# # for each project in ajax project list, check if name is in db fac_projname_list.  if not add new db entry otherwise update existing entry
#         for proj in fac_projname_list:
#             if proj in fac_projname_list:
#                 #add new entry with coordinates
#             else:
#                 #update existing entry
#
#         return_obj["project_name"] = fac_projname_list
#         return_obj["cost"] = fac_projcost_list
#         return_obj["planned_year"] = fac_projyear_list

        return JsonResponse(return_obj)

