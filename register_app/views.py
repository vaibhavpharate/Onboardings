from django.shortcuts import render
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .models import Clients, Site_Configs, SiteVerification
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# Create your views here.
@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        plan = request.POST['plan']
        client_u_check = Clients.objects.filter(username=username).count()
        if plan not in ['Premium', 'Basic', ""]:
            return JsonResponse({'error': 'Choose a valid Plan',
                                 'status_code': 403})
        if client_u_check != 0:
            return JsonResponse({'error': 'Username Already Exists',
                                 'status_code': 403})
        client_e_check = Clients.objects.filter(email=email).count()
        if client_e_check != 0:
            return JsonResponse({'error': 'Email Already Exists',
                                 'status_code': 403})
        else:
            client_short = str(username).upper()
            new_client = Clients(username=username, email=email, password=password, client_short=client_short,
                                 plans=plan)
            new_client.save()

            return JsonResponse(
                {'message': 'User Created Successfully', 'status_code': 200, 'client_id': new_client.id})


def check_lat_lon_location(lat, lon):
    indian_polygon = Polygon([(68.1, 7.9), (97.4, 7.9), (97.4, 35.5), (68.1, 35.5)])
    point = Point(lon, lat)
    return indian_polygon.contains(point)


@csrf_exempt
def create_site(request):
    if request.method == 'POST':
        site_name = request.POST['site_name']
        state = request.POST['state']
        capacity = float(request.POST['capacity'])
        type_st = request.POST['type']
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        client_id = int(request.POST['client_id'])
        client = Clients.objects.filter(id=client_id).get()
        # print()
        # client_name = client[0]['username']
        variables = request.POST['variables']

        lat_lon_check = Site_Configs.objects.filter(latitude=latitude, longitude=longitude).count()
        # Check if there is a site available at this lat lon
        if lat_lon_check != 0:
            return JsonResponse({'error': f'Site at lat:{latitude} and lon:{longitude} Already Exists',
                                 'status_code': 403})

        else:
            if check_lat_lon_location(lat=latitude, lon=longitude):

                add_site_config = Site_Configs(site_name=site_name,
                                               state=state,
                                               capacity=capacity,
                                               type=type_st,
                                               latitude=latitude,
                                               longitude=longitude,
                                               client_name=client,
                                               variables=variables)

                add_site_config.save()
                site_id = add_site_config.site_id
                verify_site = SiteVerification(
                    site_v_id=add_site_config,
                    verified=True,
                    site_status=True
                )
                verify_site.save()
                return JsonResponse({
                    'message': f'Added site with site name {site_name} for client'
                               f'with site_id {site_id}'

                })
            else:
                return JsonResponse({'error': 'Site location is outside Indian Continent',
                                     'status_code': 403})

@csrf_exempt
def delete_site(request,site_id):
    # confirm the user credentials

    # check if site exists
    # print(type(site_id))
    check_site = Site_Configs.objects.filter(site_id=site_id).count()
    if check_site == 0:
        return JsonResponse({
            'error':'The site ID does not exist',
            'status_code': 403
        })
    else:
        site_verification = SiteVerification.objects.get(site_v_id=site_id)
        site_verification.site_status = False
        site_verification.save()
        return JsonResponse({
            'Message': f'Deleted the Site with site id {site_id}',
            'status_code': 200
        })
