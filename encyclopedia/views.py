from logging import PlaceHolder
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import randint
from . import util
import markdown2
import re


#Create a new page form
class newPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter title of the page', 'class':'form-control'}))
    data = forms.CharField(label="Data", widget=forms.Textarea(attrs={'placeholder': 'Enter your page data here','class':'form-control', 'style':'white-space: pre-wrap;'}))
    
#Form for searchbox
class searchForm(forms.Form):
    searchField = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search title', 'class':'form-control' }))

#defining a searchform instance
searchform = searchForm()

#Search Function for sidebar
def Search(request,entries):
    #populating the form
    newsearch = searchForm(request.POST)
    newlist = []
    if newsearch.is_valid():

        #cleaning the search field 
        newsearch = newsearch.clean()
        
        #searching through titles
        for page in entries:
            if page.find(newsearch['searchField']) != -1:
                newlist.append(page)
        return newlist 
        

            
#handling index page 
def index(request):
    entries = util.list_entries()
    #handling POST method 
    if request.method == "POST":
        #if randompage button is clicked 
        if "randompage" in request.POST:    
            return HttpResponseRedirect("/wiki/" + entries[randint(0, len(entries) - 1)])

        #calling search function
        entries = Search(request, entries)

        #if no entries are found show error page 
        if entries == 0:
            return render(request, "encyclopedia/404.html", {
                "searchform":searchform
            })    
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "searchform": searchform
            })
        
    #Handling GET method 
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "searchform": searchform
        })

#Handling all the page entries
def pages(request, name):
    #returns the list of entries 
    entries = util.list_entries()

    if request.method == "POST":
        #if randompage button is clicked 
        if "randompage" in request.POST:    
            return HttpResponseRedirect("/wiki/" + entries[randint(0, len(entries) - 1)])
            
    else:
        #checking if name in entries exist or not 
        if name in entries:
            file = util.get_entry(name)
            if file:
                #converting markdown to html and feeding the data in pages.html
                html = markdown2.markdown(file)
                return render(request, "encyclopedia/pages.html", {
                    "name": name,
                    "file": html
                })
            else:
                return render(request, "encyclopedia/404.html", {
                    "searchform":searchform
                })
        else:
            return render(request, "encyclopedia/404.html", { 
                "searchform":searchform
            })

#Handling Create new page
def createpage(request):
    createpageForm = newPage()
    entries = util.list_entries()
    if request.method == "POST":
        #if randompage button is clicked 
        if "randompage" in request.POST:    
            return HttpResponseRedirect("/wiki/" + entries[randint(0, len(entries) - 1)])

        #Populating the form
        newpage = newPage(request.POST)

        #checking if the form is valid 
        if newpage.is_valid():
            #cleaning the input data
            newpage = newpage.clean()
            
            #checking if the entry already exists
            if util.get_entry(newpage['title']) == None:
                #Since the contents only get written to the file, We have to add title as well
                util.save_entry(newpage['title'],"# " + newpage['title'] + "\n\n" + newpage['data'])
                
                #redirecting to the newlyformed page
                return HttpResponseRedirect("/wiki/" + newpage['title'])
            else:
                #rendering error
                return render(request, "encyclopedia/createpage.html", {
                "createpageForm" : createpageForm,
                "label" : "The entry already exists!" 
                })

    else:
        return render(request, "encyclopedia/createpage.html", {
            "createpageForm" : createpageForm 
        })

#Handling edit page 
def editpage(request, name):
    entries = util.list_entries()
    editpageForm = newPage()
    if request.method == "POST":
        #if randompage button is clicked 
        if "randompage" in request.POST:    
            return HttpResponseRedirect("/wiki/" + entries[randint(0, len(entries) - 1)])

        #Populating the form
        editedpage = newPage(request.POST)
        
        #checking if the form is valid 
        if editedpage.is_valid():
            #cleaning the input data
            editedpage = editedpage.clean()
            print(editedpage['data'])
            util.save_entry(editedpage['title'], editedpage['data'])

            #redirecting to the edited page
            return HttpResponseRedirect("/wiki/" + editedpage['title'])
    else:
        #Getting and updating the editpageForm 
        editpageForm = newPage(initial={'title':name, 'data':util.get_entry(name)})
        print(util.get_entry(name))
        return render(request, "encyclopedia/editpage.html", {
                "editpageForm" : editpageForm,
                "name": name,
            })