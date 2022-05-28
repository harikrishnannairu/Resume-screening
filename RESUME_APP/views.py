from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from pkg_resources import Requirement
from .models import *
from PyPDF2 import PdfFileReader
from gensim.parsing.preprocessing import remove_stopwords 
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from gensim.summarization import summarize
from sklearn.neighbors import NearestNeighbors
import operator

# Create your views here.

##############LOGIN & REGISTER START###########
def register(request):
    return render(request, 'register.html',{})

def check_register(request):
    username = request.GET.get("uname")
    password1 = request.GET.get("pass1")
    password2 = request.GET.get("pass2")
    first_name = request.GET.get("fname")
    last_name = request.GET.get("lname")
    email = request.GET.get("email")
    if User.objects.filter(username=username).exists():
        print("UIsername already taken")
        #messages.info(request,'Username already taken')

        #return redirect('register')
        return HttpResponse("Username already taken")
    elif User.objects.filter(email=email).exists():
            
       # messages.info(request,"Email already taken")
            #messages.add_message(request, messages.INFO, 'Email already taken')
        #return redirect('register')
        return HttpResponse("Email already taken")
    else:
        if password1==password2:

            user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
            user.save()
            print("User created")
               # return render(request,"index.html")
            return HttpResponse("HR Registration Successfull")
                
        else:
            print("Password doesnt match") 
            #messages.info(request,'password doesnt match')
            return HttpResponse("Password does not match")

#####################################
def display_login_first(request):
    return render(request, "login.html", {})
def display_login(request):
    return render(request, "login.html", {})


def check_login(request):
    username = request.GET.get("uname")
    password = request.GET.get("pass")
    
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponse("HR Login Successful")
   # print(username)
   # print(password)

   # if username == 'ADMIN' and password == 'ADMIN':
  #      return HttpResponse("HR Login Successful")
  #  else:
  #      return HttpResponse("Invalid")

     

##############LOGIN & REGISTER END#############

# ADMIN START


def a_home_hr(request):
    return render(request, "home_hr.html", {})


def b_upload_resume_hr(request):
    return render(request, "upload_resume_hr.html", {})


def upload_resume(request):
    file_name = request.POST.get("f_upload")
    file1 = request.FILES["f_upload"]
    print("<<<<<<<<<<<<<<<<<", file1)

    candidate_name = request.POST.get("a_name")
    print(candidate_name)

    file = file1

    fs = FileSystemStorage("RESUME_APP\\static\\files_upload")
    fs.save(file_name, file)

    k = Resumes.objects.filter(
        candidate_name=candidate_name, file=file)
    c = k.count()
    if c == 1:
        print("[INFO]: Resume already submitted")
        return HttpResponse("[INFO]: Resume already submitted")
    else:
        a = Resumes(
            candidate_name=candidate_name, file=file)
        a.save()
        print("[INFO]: Resume uploaded successfully")

        return render(request, "upload_resume_hr.html")


def c_view_resume_hr(request):
    return render(request, "view_resume_hr.html", {})


def resumes(request):
    d = Resumes.objects.all()
    # print(d)
    dic = {}
    if d:
        value = serializers.serialize("json", d)
        dic["key"] = json.loads(value)
        # print(dic)
        return JsonResponse(dic, safe=False)
    else:
        return HttpResponse("No assignments")


def delete(request):
    candidate_name = request.GET.get("cname")

    f = Resumes.objects.get(candidate_name=candidate_name)
    f.delete()
    return HttpResponse("Resume Deleted Successfully")


def d_resume_screen_hr(request):
    return render(request, "resume_screen_hr.html", {})

def store(request):
    candidate_name=c_name
    file=k
    resume_score=v

    vv=Screen(candidate_name=candidate_name,file=file,resume_score=resume_score)
    vv.save()

def retrieve(request):
    
    tt=Screen.objects.all()
    global dicc
    dicc={}
    if tt:  
        value = serializers.serialize("json", tt)
        dicc["key"] = json.loads(value)
        # print(dicc)
        return JsonResponse(dicc, safe=False)
    else:
        return HttpResponse("No records")  


def perform(request):
    req = request.GET.get("req")

    resume_names_dict = Resumes.objects.values('file')
    print("Resume List (DICTIONARY)>>>>>>", resume_names_dict)
    job_req=0
    resume_names_list = [i["file"] for i in resume_names_dict]
    print("list_of_Resume_name>>>>>>", resume_names_list)

    ordered_list_resume=[]
    ordered_list_resume_score=[]
    resume_vector=[]
    temp_pdf=[]
    allresumes=[]
    for i in resume_names_list:
        ordered_list_resume.append(i)
        print("RESUME NAME -------------------------->>>>:",i)
        reader = PdfFileReader(open(i,'rb'))
        pages = reader.getNumPages()
        print("pages:>>>>>> ",pages)
        for page_number in range(pages):
            page = reader.getPage(page_number)
            text = page.extractText()
            text=text.replace('\n',' ')
            text=re.sub("\s\s+",' ',text)#remove multiple spaces
            print("text:",text)
            temp_pdf=str(temp_pdf) + str(text)
        allresumes.extend([temp_pdf])
        temp_pdf=''
    print("allresumes:>>>>>>>>>>>>>>>>",allresumes)

    req_a=str(req)
    req_a=summarize(req_a,ratio=0.5)
    print("summarized requirement:::>>>>>>>>>>>>",req_a)
    req=[req_a]

    vectorizer=TfidfVectorizer(stop_words='english')
    vectorizer.fit(req)
    vector=vectorizer.transform(req)

    job_req=vector.toarray()


    for i in allresumes:
        text=i
        text_str=str(text)
        text_str=summarize(text_str,ratio=0.5)
        print("summarized resume ::::::>>>>>>>",text_str)
        text=[text_str]
        vector= vectorizer.transform(text)

        var=vector.toarray()
        resume_vector.append(vector.toarray())

    for i in resume_vector:
         samples=i
         neigh=NearestNeighbors(n_neighbors=1)
         neigh.fit(samples)
         NearestNeighbors(algorithm='auto',leaf_size=30)

         ordered_list_resume_score.extend(neigh.kneighbors(job_req)[0][0].tolist())

    final=[z for _,z in sorted(zip(ordered_list_resume_score,ordered_list_resume))] #showing resume name increasing order of score
    # print(final)
    print("Ordered list resume:::>>>>>>>",ordered_list_resume)
    print("Ordered list resume score:::>>>>>>>",ordered_list_resume_score)

    my_dict=dict(zip(ordered_list_resume,ordered_list_resume_score))
    print(my_dict)

    sorted_my_dict=dict(sorted(my_dict.items(),key=operator.itemgetter(1)))
    print("sorted my_dict::>>>>",sorted_my_dict)

    global k
    global v
    for k,v in sorted_my_dict.items():
        
        print("resume name",k)
       
        print("resume rank",v)
        global c_name
        r_name=Resumes.objects.get(file=k)
        c_name=r_name.candidate_name
        print(c_name)

        request=0
        store(request)
    retrieve(request)

    return JsonResponse(dicc,safe=False)

def table_delete(request):
    a = Screen.objects.all().delete()

    return HttpResponse("Temporary Screen Table Values Deleted")






    













    
    # req = request.GET.get("req")
    # req=req.lower()
    # req=re.sub(r"[^a-zA-Z. @0-9]+",' ',req)#remove special chqaracters except (. @a-zA-Z0-9)
    # req=re.sub("\s\s+",' ',req)#remove multi-spaces
    # req=remove_stopwords(req)
    # print(req)

    # resume_names_dict = Resumes.objects.values('file')
    # print("Resume List (DICTIONARY)>>>>>>", resume_names_dict)

    # resume_names_list = [i["file"] for i in resume_names_dict]
    # print("list_of_Resume_name>>>>>>", resume_names_list)

    # allresumes = []
    # for i in resume_names_list:
    #     print("RESUME NAME -------------------------->>>>:",i)
    #     reader = PdfFileReader(open(i,'rb'))
    #     pages = reader.getNumPages()
    #     print("pages:>>>>>> ",pages)
    #     page = reader.getPage(0)
    #     text = page.extractText()
    #     # print(text)
    #     # print(type(text))
    #     text=text.replace("\n","")
    #     text=text.lower()
    #     text=re.sub(r"[^a-zA-Z. @0-9]+",' ',text)
    #     print("AFTER SPECIAL characters removal:::>>>>",text)
    #     # print("Before:::>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",text)
    #     text=re.sub("\s\s+",' ',text)#remove multiple spaces
    #     print("AFTER:::::::::::::::::::::::::>>>>>>>>>>>>>>>>",text)

        

    #     text=remove_stopwords(text)
    #     print("after stop words removal:::::::>>>>>>>>",text)
    #     list=[]
    #     list.append(text)


    #     allresumes.append(list)
    # print("allresumes::::::::>>",allresumes)
    # print("length allresumes:>>>>>>>>>>>>>>>", len(allresumes))
    # print("req:::>>>",req)

    
    # #adding requirements with the resumes
    # my_req=req 
    # my_req=[my_req]
    # print("my_req_list:::>",my_req)
    # allresumes.append(my_req)
    # print("allresumes after REQUIREMENT::::::::>>",allresumes)
    # print("length allresumes after REQUIREMENT:>>>>>>>>>>>>>>>", len(allresumes))

    # new_allresumes=[]   #for convert the list of lists --->list of items (for tf-idf vectorizer fit input)
    # for l in allresumes:
    #     # print(l)
    #     l1=l[0]
    #     # print(l1)
    #     new_allresumes.append(l1)
    #     # print("*********************************************************************")
    # print("NEW_ALLRESUMES::>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",new_allresumes)

    # vectorizer=TfidfVectorizer()
    # # result=vectorizer.fit(new_allresumes)#both requirements(req) and resumes(allresumes)
    # result=vectorizer.fit(new_allresumes)

    # final_result=vectorizer.transform([req])
    # print(final_result)
    # final_array=final_result.toarray() # array representation
    # print(final_array)

    # df=pd.DataFrame(final_array,columns=vectorizer.get_feature_names())
    # print(df)

    # print("before remove::((((((((",allresumes)
    # print(req)
    # allresumes.remove([req])
    # print("after remove: WITHOUT REQUIREMENT:)))))))))))))))))",allresumes)
    # print("LENGTH:::::",len(allresumes))

    # cosine_list=[]
    # for z in allresumes:
    #     print("its my resume name:@@@@@@@@@@@@@@@@@@@@@@@@@",z)
    #     each_file=vectorizer.transform(z)
    #     each_file_array=each_file.toarray()

    #     df1=pd.DataFrame(each_file_array,columns=vectorizer.get_feature_names())
    #     print(df1)

    #     cosine=cosine_similarity(df,df1)
    #     print("Cosine Similarity------------------------------------------",cosine)
    #     cosine_list.append(cosine)
    # print("Cosine_List:::>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",cosine_list)
    # print("type of cosine list", type(cosine_list))


























    # import spacy
    # from spacy.matcher import Matcher

    # # load pre-trained model
    # nlp = spacy.load('en_core_web_sm')

    # # initialize matcher with a vocab
    # matcher = Matcher(nlp.vocab)

    # for k in allresumes:
    #     kk=k[0]
    #     nlp_text = nlp(kk)
        
    #     # First name and Last name are always Proper Nouns
    #     pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        
    #     # matcher.add('NAME', None, *pattern)
    #     matcher.add(kk, [pattern])

    #     matches = matcher(nlp_text)
        
    #     for match_id, start, end in matches:
    #         span = nlp_text[start:end]
    #         print(span.text)

    return HttpResponse("done")
