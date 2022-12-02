from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import views, status
import socket
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password , check_password
from . import models
from . import serializers

import xlsxwriter
import datetime 
from django.http import HttpResponse

# Create your views here.

@api_view(('GET',))
def index(request):
    return render(request,'index.html')



class addCompany(views.APIView):
   
    def post(self, request):
        data = request.data
        print("data",data)
        user_serializer = serializers.CountrySerializer(data=data)
        place = request.data.get('place',None)
        family = models.Country.objects.filter(place=place).exists()
        if family is False:
            if user_serializer.is_valid():
                user_serializer.save(is_verified=True,name=place)
                return JsonResponse({"success":"Country Added Successfully " + place},safe=False)
            else:
                print("user_serializer",user_serializer.errors)
                return JsonResponse({"error":user_serializer.errors},safe=False)
        return Response({"error":place +" Country Already Exists"},400)
class addState(views.APIView):
   
    def post(self, request):
        data = request.data
        print("data",data)
        user_serializer = serializers.StateSerializer(data=data)
        place = request.data.get('place',None)
        country = request.data.get('countryname',None)
        css = models.Country.objects.filter(name=country)
        family = models.State.objects.filter(place=place,country=css).exists()
        if family is False:
            if user_serializer.is_valid():
                user_serializer.save(country=css,name=place)
                return JsonResponse({"success":"State Added Successfully" + place},safe=False)
            else:
                print("user_serializer",user_serializer.errors)
                return JsonResponse({"error":user_serializer.errors},safe=False)
        return Response({"error":place +" State Already Exists"},400)

class companyList(views.APIView):
    
    def get(self,request):
        user = models.Country.objects.filter()
        serialize = serializers.CountrySerializer(user, many=True)
        return Response({'serializer': serialize.data})

class companyDetails(views.APIView):
    
    def get(self,request,id=0):
        user = models.Country.objects.filter(id=id)
        serialize = serializers.CountrySerializer(user, many=True)
        return Response({'company': serialize.data})
        
class comstateList(views.APIView):
    
    def get(self,request,id=0):
        user = models.State.objects.filter(country__id=id)
        serialize = serializers.StateSerializer(user, many=True)
        return Response({'serializer': serialize.data})

class AdminRegister(views.APIView):
   
    def post(self, request):
        data = request.data
        print("data",data)
        user_serializer = serializers.userSerializer(data=data)
        email = request.data['email']
        family = models.User.objects.filter(email=email).exists()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname) 
        if family is False:
            if user_serializer.is_valid():
                raw_password = user_serializer.password = make_password(user_serializer.validated_data['password'])
                user_serializer.save(password=raw_password,userType="admin")
                id = models.User.objects.filter(email=email).values()
                data1 = {}
                origins = settings.BACKEND_URL
                data1['email']= email
                userid = id[0]['access_token']
                data1['origin'] = origins
                data1['userid'] = userid
                html_message = render_to_string('admin_verifyregister.html',{'context':data1})
                send_mail(
                        'Gateway Md Registration',
                        "Verify Email",
                        settings.EMAIL_HOST_USER,
                        [email],
                        html_message=html_message,
                ) 
                return JsonResponse({"success":"Registered Succesfully ,verify link sent to " + email},safe=False)
            else:
                print("user_serializer",user_serializer.errors)
                return JsonResponse({"error":user_serializer.errors},safe=False)
        return Response({"error":email +" email Already Exists"},400)


class AdminRegisterVerify(views.APIView):
    def get(self,request,id=None):
        origins = settings.CORS_ALLOWED_ORIGINS
        origin = origins[0]
        if id:
            models.User.objects.filter(access_token=id).update(is_active=True)
        return redirect(origin)


class AdminLogin(views.APIView):

    def post(self,request):
        data=request.data    
        print("data",data)
        # MembershipID = data['MembershipID']
        email = data['email']
        print("email",email)
        password = (request.data.get("password",None))
        print("password",password)
        user = models.User.objects.filter(email=email).exists()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if user:
            useractiveasd = models.User.objects.filter(email=email,is_expire=True).exists()
            if useractiveasd:
                return JsonResponse("User is InActive " + email,safe=False)
            else:                  
                useractive = models.User.objects.filter(email=email,is_active=True).exists()
                if useractive:
                    user1 = models.User.objects.filter(email=email).values()
                    pwd_valid = check_password(password,user1[0]['password'])
                    if pwd_valid is True:
                        return Response({"Success":"Login Succesfully","data":user1[0]})
                    else:
                        return JsonResponse("Invalid Credentials. Incorrect Password",safe=False)                
                else:                  
                    return JsonResponse("Activation link Sent to Your email " + email,safe=False)                
        else:
            return JsonResponse("Email Doesn't Exists "+email,safe=False)


class AccessADMINtoken(views.APIView):

    def get(self,request,id=0):
        print("id",id)
        users = models.User.objects.filter(access_token=id).exists()
        if users:            
            user = models.User.objects.get(access_token=id)
            serializer = serializers.userSerializer(user)        
            return Response(serializer.data)
        else:       
            return Response("No Access Token Found")


class AdminUpdate(views.APIView):

    def put(self, request,id=0):
        data=request.data
        print("id for Admin request",id,data)
        email = request.data.get("email",None)
        emailexist = models.User.objects.filter(email=email).exists()
        family =  models.User.objects.get(id=id)
        emails = family.email
        if emails != email:
            if emailexist:
                return JsonResponse({"error":"Email Already Exists "+ email},safe=False)
        family_serializer = serializers.userSerializer(family, data=data)
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname) 
        if family_serializer.is_valid():
            old_data = list(models.User.objects.filter(id=id).values()) 
            family_serializer.save(is_active=True,is_verified=True)
            new_data = list(models.User.objects.filter(id=id).values())
            return JsonResponse("Updated Successfully",safe=False)
        else:
            print(".errors",family_serializer.errors)
            return JsonResponse(family_serializer.errors,safe=False)


class PasswordUpdateAdmin(views.APIView):

    def post(self, request,id=0):
        print("data",request.data , id)
        data = request.data
        currentPassword = data['currentPassword']
        family =  models.User.objects.get(id=id)
        usersp = check_password(currentPassword, family.password)
        if usersp == True:
            user_serializer = serializers.userSerializer(family, data=data)
            if user_serializer.is_valid():
                raw_password = make_password(user_serializer.validated_data['password'])
                family.password = raw_password
                family.save()
                return JsonResponse({"success":"Password Updated Succesfully"},safe=False)
            else:
                return JsonResponse(user_serializer.errors,safe=False)
        else:
            return Response({"error":"Current Password is Incorrect"})


class Adminresetpass(views.APIView):

    def post(self, request,id=0):
        if id:
            check = models.User.objects.filter(access_token=id).exists()
            if check:
                user1 = models.User.objects.filter(access_token=id).values()
                data = request.data
                print("data",data)
                password  = data['password']
                user_serializer = serializers.userSerializer(user1, data=data)
                if user_serializer.is_valid():
                    raw_password = make_password(user_serializer.validated_data['password'])
                    user =  models.User.objects.get(access_token=id)
                    user.password = raw_password
                    user.is_active=True
                    user.save()
                    print("id",id)
                return Response({"success":"Password Updated Successfully"})
            else:
                return Response({"error":"Invalid Link"})
        else:
            origin = settings.CORS_ALLOWED_ORIGINS
            data = request.data
            print("data",data)
            email = data['email']
            check =  models.User.objects.filter(email=email,is_verified=True).exists()
            if check:
                id = models.User.objects.filter(email=email).values()
                data1={}
                origin = settings.CORS_ALLOWED_ORIGINS
                userid = id[0]['access_token']
                data1['userid'] = userid
                data1['email'] = email
                data1['origin'] = origin[0]
                print("check", userid , data)
                html_message = render_to_string('admin_forgetpassword.html',{'context':data1})
                send_mail(
                    'Password Reset',
                    "Confirm Password",
                    settings.EMAIL_HOST_USER,
                    [email],
                    html_message=html_message,
                )
                print("mail",send_mail)
                return Response({"success":'Password reset e-mail has been sent to ' + email})
            else:
                return Response({"error":"Email Does't Exists " + email})
        

class alluseremail(views.APIView):
    def get(self,request,id=None):
        email = models.User.objects.values_list('email', flat=True).distinct()
        return JsonResponse({"email":list(email)},safe=False)


class deletemployee(views.APIView):

    def post(self,request):
        data = request.data
        print("data",data)
        loginuser = data['loginuser']
        id = data['id']
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        superadmin = models.User.objects.get(access_token=loginuser)
        models.User.objects.filter(id=id).update(is_active=False,is_verified=False,is_expire=True)
        return JsonResponse("Delete Successfully.", safe=False)


class activeemployee(views.APIView):

    def post(self,request):
        data = request.data
        print("data",data)
        loginuser = data['loginuser']
        id = data['id']
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        superadmin = models.User.objects.get(access_token=loginuser)
        models.User.objects.filter(id=id).update(is_active=True,is_verified=True,is_expire=False)
        return JsonResponse("Activated Successfully.", safe=False)


class adminlistdownload(views.APIView):
    def get(self,request):
        data = models.User.objects.all().order_by('-created_at')
        serializer = serializers.userSerializer(data , many=True)
        date = datetime.datetime.now().strftime ("%Y-%m-%d")
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename = User_List ' + str(date) + '.xlsx'
        response['Access-Control-Expose-Headers']= response['Content-Disposition']
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        # Add an Excel date format.
        title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'fg_color': '#79eb3b',
        'align': 'center',
        'valign': 'vcenter'
        })
        worksheet.merge_range('A1:J1', "Gatewat Md", title)
        # Adjust the column width.
        # worksheet.set_column(1, 1, 25)
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 35)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 15)
        header_format = workbook.add_format({
                'bold': True,
                'fg_color': '#00BFFF', # F7F7F7 #00BFFF
                'align': 'center',
                'border': 1})
        # Write some data headers.
        worksheet.write('A2', 'First Name', header_format)
        worksheet.write('B2', 'Last Name', header_format)
        worksheet.write('C2', 'Contact Phone', header_format)
        worksheet.write('D2', 'Email', header_format)
        worksheet.write('E2', 'Address', header_format)
        worksheet.write('F2', 'City', header_format)
        worksheet.write('G2', 'State', header_format)
        worksheet.write('H2', 'Zipcode', header_format)
        worksheet.write('I2', 'Status', header_format)
        worksheet.write('J2', 'Type', header_format)
    
        row = 2
        col = 0
        for row_num, columns, in enumerate(serializer.data):
            worksheet.write(row, col, columns['firstName'],bold)
            worksheet.write(row, col+1, columns['lastName'],bold)
            worksheet.write(row, col+2, columns['contactPhone'],bold)
            worksheet.write(row, col+3, columns['email'],bold)
            worksheet.write(row, col+4, columns['address1'],bold)
            worksheet.write(row, col+5, columns['city'],bold)
            worksheet.write(row, col+6, columns['state'],bold)
            worksheet.write(row, col+7, columns['zipcode'],bold)
            if columns['is_active'] == True:
                status = "Active"
            else:
                status = "Not Active"
            worksheet.write(row, col+8, status,bold)
            if columns['accType'] == "superadmin":
                acctype = "Super Admin"
            if columns['accType'] == "admin":
                acctype = "Admin"
            if columns['accType'] == "manager":
                acctype = "Manager"
            if columns['accType'] == "generaluser":
                acctype = "General User"
            worksheet.write(row, col+9, acctype,bold)
            row += 1

        workbook.close()   
        return response


class stateList(views.APIView):

    def get(self,request):
        return Response({"state":models.STATE})


class ADMINUpdate(views.APIView):

    def put(self, request,id=0):
        data=request.data
        print("id for admin request",id,data)
        email = request.data.get("email",None)
        password = request.data.get("password",None)
        emailexist = models.User.objects.filter(email=email).exists()
        family =  models.User.objects.get(id=id)
        emails = family.email
        if emails != email:
            if emailexist:
                return JsonResponse({"error":"Email Already Exists "+ email},safe=False)
        family_serializer = serializers.userSerializer(family, data=data)
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname) 
        if family_serializer.is_valid():
            old_data = list(models.User.objects.filter(id=id).values()) 
            family_serializer.save(is_active=True,is_verified=True)
            new_data = list(models.User.objects.filter(id=id).values())
            return JsonResponse("Updated Successfully",safe=False)
        else:
            print(".errors",family_serializer.errors)
            return JsonResponse(family_serializer.errors,safe=False)

class PasswordUpdateAdmin(views.APIView):

    def post(self, request,id=0):
        print("data",request.data , id)
        data = request.data
        currentPassword = data['currentPassword']
        family =  models.User.objects.get(id=id)
        usersp = check_password(currentPassword, family.password)
        if usersp == True:
            user_serializer = serializers.userSerializer(family, data=data)
            if user_serializer.is_valid():
                raw_password = make_password(user_serializer.validated_data['password'])
                family.password = raw_password
                family.save()
                return JsonResponse({"success":"Password Updated Succesfully"},safe=False)
            else:
                return JsonResponse(user_serializer.errors,safe=False)
        else:
            return Response({"error":"Current Password is Incorrect"})

class userDetails(views.APIView):
    
    def get(self,request):
        user = models.User.objects.filter(is_active=True)
        serialize = serializers.userSerializer(user, many=True)
        return Response({'serializer': serialize.data})