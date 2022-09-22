#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import re # regular expression
import time

from Tools import tools_v000 as tools
from os.path import dirname
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# -4 for the name of this project Jira
#save_path = dirname(__file__)[ : -4]
save_path = os.path.dirname(os.path.abspath("__file__"))[ : -4]
propertiesFolder_path = save_path + "\\"+ "Properties"

# Example of used
# user_text = tools.readProperty(propertiesFolder_path, 'Jira', 'user_text=')

# ====================================================================
# URL 
# https://regex101.com/
# https://regexr.com/
# ====================================================================

incidentNumber = ""
incidentTitle = ""
description_text = ""
save_path = ""

jiraTitle = ""
contact_id = ""
user_name = ""

jira = ""

sprint = ""
epic_link = ""

delay_properties = 10

def connectToJira(jira) :
    tools.driver.get("https://jira.atlassian.insim.biz/browse/" + jira)

def connectToJiraTST(jira) :
    tools.driver.get("https://jira-test.atlassian.insim.biz/browse/" + jira)

# since the 07-06-2022 the SSO is not working anymore.
# Then need to place the credential
# Since the 01-08-2022 the SSO is working back for PRD but not for TST
def loginToJira(url, user, password) :    
    tools.driver.get(url)
    # User
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="login-form-username"]')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="login-form-username"]')
    projectInput.send_keys(user)
    
    # Password
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="login-form-password"]')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="login-form-password"]')
    projectInput.send_keys(password)
    
    
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="login-form-submit"]')
    projectInput = tools.driver.find_element_by_xpath('//*[@id="login-form-submit"]')
    projectInput.click()
    
def recoverJiraInformation() :
    # jiraTitle
    global jiraTitle
    tools.waitLoadingPageByID("summary-val")
    time.sleep(1)
    jiraTitle = tools.driver.find_element_by_id("summary-val").text
    # print("jiraTitle : " + jiraTitle)
    
    # incidentNumber
    global incidentNumber
    incidentNumber = re.findall(r"[I]{1}\d{4}-{1}\d{5}",jiraTitle)
    if not incidentNumber:
        incidentNumber = ""
    else:
        incidentNumber = incidentNumber[0]
    # print("incidentNumber : " + incidentNumber)
    
    # incidentTitle
    global incidentTitle
    if len(incidentNumber) == 0 : 
        incidentTitle = jiraTitle
    else : 
        incidentTitle = jiraTitle[14:]
    # print("incidentTitle : " + incidentTitle)

    # description_text
    global description_text 
    tools.waitLoadingPageByID("description-val")
    description_text = tools.driver.find_element_by_id("description-val").text.encode('utf-8', 'ignore')
    try :
        print("description_text : " + description_text )
    except UnicodeEncodeError as ex :
        print("UnicodeEncodeError : ")
        description_text = "Error to take the description"
        pass

    # contact_id
    global contact_id
    if len(incidentNumber) == 0 : 
        contact_id = ""
    else : 
        contact_id = re.findall(r"\d{7}",jiraTitle)
        if not contact_id :
            contact_id = ""
        else :
            contact_id = contact_id[0]
    # print("contact_id : " + contact_id)

    # user_name
    global user_name
    if len(incidentNumber) == 0 : 
        user_name = ""
    else : 
        user_name = re.findall(r"[a-zA-Z]*[.][a-zA-Z]*",jiraTitle)
        if not user_name :
            user_name = ""
        else :
            user_name = user_name[0]
    # print("user_name : " + user_name)

    # Epic Link
    global epic_link
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="customfield_10008-val"]/a')
    epic_link = tools.driver.find_element_by_xpath('//*[@id="customfield_10008-val"]/a').text
    print ("epic_link : " + epic_link)


def createFolderJira(jira) :
    if os.path.isdir(save_path + jira) :
        print ("Folder already exist")
    else :
        os.mkdir(save_path + jira)

def createFileInto(jira, jiraTitle, description_text, path, name_of_file ) :
    completeName = os.path.join(save_path + path, name_of_file+".txt")

    if os.path.isfile(completeName) :
        file1 = open(completeName, "a+")
        file1.write("\n")    
        file1.write("========================================================================================================================"+"\n")
        file1.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        file1.write("\n")
    else :
        file1 = open(completeName, "w")

        file1.write("\n")    
        file1.write("========================================================================================================================"+"\n")
        file1.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        file1.write("\n")
        file1.write(jiraTitle.encode('utf-8').strip() + "\n")
        file1.write("\n")
        try :
            file1.write(description_text + "\n")
        except UnicodeEncodeError :
            file1.write("Not possible to place the description for the moment")
        file1.write("\n")
        if len(contact_id) == 0 :
            file1.write("\n")
        else :
            file1.write("contact_id = " + contact_id + "\n")
        if len(user_name) == 0 :
            file1.write("\n")
        else :
            file1.write("user_name = " + user_name + "\n")
        
        if len(contact_id) > 0 or len(user_name) > 0 :
            file1.write("ToBeTreated = True" + "\n")

        file1.close() 

def startJira() :
    tools.waitLoadingPageByID("opsbar-transitions_more")
    workflow = tools.driver.find_element_by_id("opsbar-transitions_more")
    workflow.click()
    
    # 
    tools.waitLoadingPageByID("action_id_51")
    workflow = tools.driver.find_element_by_id("action_id_51")
    workflow.click()

    time.sleep(1)

def selectJira() :
    tools.driver.get("https://jira.atlassian.insim.biz/secure/RapidBoard.jspa?rapidView=464&quickFilter=1705")

    # forced the refresh of the page => due to a bug when you create the jira it's not appear directly in the list
    tools.driver.refresh()      
    
    global jira
    try :
        # Normal ticket
        tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/div/ul/li[1]/div/div[1]/div[1]/div[1]/a")
        jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/div/ul/li[1]/div/div[1]/div[1]/div[1]/a")                                                         
        jira_link.click()
        
        tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/header/div[1]/div[3]/dl/dd/a")
        jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/header/div[1]/div[3]/dl/dd/a")                     
        jira_link.click()

        tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/header/div/header/div/div[2]/ol/li[2]/a")
        jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/header/div/header/div/div[2]/ol/li[2]/a")   
        jira = jira_link.text
    except :
        try :
            # subtask from a ticket
            tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/div/ul/li[1]/div/div[2]/div/div[1]/div")
            jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[1]/div[2]/div/ul/li[1]/div/div[2]/div/div[1]/div")                                                         
            jira_link.click()
        
            tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/header/div[1]/div[3]/dl/dd/a")
            jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div[2]/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/header/div[1]/div[3]/dl/dd/a")                     
            jira_link.click()

            tools.waitLoadingPageByXPATH("/html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/header/div/header/div/div[2]/ol/li[3]/a")
            jira_link = tools.driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/header/div/header/div/div[2]/ol/li[3]/a")
            jira = jira_link.text

        except :
            tools.driver.quit()


def createJira(jiraTitle, description_text, incidentNumber, teamName) :
    tools.waitLoadingPageByID("create_link")
    create_link = tools.driver.find_element_by_id("create_link")
    create_link.click()
    # Project
    tools.waitLoadingPageByID("project-field")
    project_field = tools.driver.find_element_by_id("project-field")
    project_field.click()
    project_field.send_keys(teamName)
    project_field.send_keys(Keys.ENTER)
    
    time.sleep(1)
    
    # Issue Type
    tools.waitLoadingPageByID2(20,"issuetype-field")
    issuetype_field = tools.driver.find_element_by_id("issuetype-field")
    issuetype_field.click()
    issuetype_field.send_keys("User Story")
    issuetype_field.send_keys(Keys.ENTER)
    time.sleep(1)

    # Summary
    tools.waitLoadingPageByID("summary")
    summary = tools.driver.find_element_by_id("summary")
    summary.send_keys(jiraTitle)
    time.sleep(1)

    # Description
    tools.waitLoadingPageByID("description")
    description = tools.driver.find_element_by_id("description")
    description.send_keys(incidentNumber + "\n")
    if (incidentNumber.startswith('INC')) :
        description.send_keys("https://nn.service-now.com/text_search_exact_match.do?sysparm_search=" + incidentNumber + "\n")
    else :
        description.send_keys("https://nn.service-now.com/text_search_exact_match.do?sysparm_search=" + incidentNumber + "\n")
    time.sleep(1)

    # assign to me
    tools.waitLoadingPageByID("assign-to-me-trigger")
    assign_to_me_trigger = tools.driver.find_element_by_id("assign-to-me-trigger")
    assign_to_me_trigger.click()
    time.sleep(1)
    
    # # Need to go down of the page
    # tools.waitLoadingPageByID("description")
    # description = tools.driver.find_element_by_id("description")
    # description.send_keys(Keys.PAGE_DOWN)

    # sprint
    tools.waitLoadingPageByID("customfield_10007-field")
    customfield_10007 = tools.driver.find_element_by_id("customfield_10007-field")
    customfield_10007.send_keys(sprint)
    time.sleep(1)
    customfield_10007.send_keys(Keys.ENTER)
    time.sleep(1)

    # #Need to go Up of the page
    # tools.waitLoadingPageByID("description")
    # description = tools.driver.find_element_by_id("description")
    # description.send_keys(Keys.PAGE_UP)

    # --------------------- Link ----------------------
    tools.waitLoadingPageByXPATH("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[2]/a/strong")
    link_button = tools.driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[2]/a/strong")
    link_button.click()

    time.sleep(1)

    # Epic Link
    tools.waitLoadingPageByID("customfield_10008-field")
    customfield_10008 = tools.driver.find_element_by_id("customfield_10008-field")
    customfield_10008.click()
    customfield_10008.send_keys(epic_link)    
    time.sleep(1)
    customfield_10008.send_keys(Keys.ARROW_DOWN)    
    customfield_10008.send_keys(Keys.ENTER)    

    # Labels
    tools.waitLoadingPageByID("labels-textarea")
    labels_textarea = tools.driver.find_element_by_id("labels-textarea")
    labels_textarea.send_keys("IT4IT")
    labels_textarea.send_keys(Keys.ENTER)
    time.sleep(1)
    # ---------------- References ---------------------
    tools.waitLoadingPageByXPATH("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[3]/a/strong")
    reference_button = tools.driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[3]/a/strong")
    reference_button.click()

    # Topdesk reference
    tools.waitLoadingPageByID("customfield_12600")
    topdesk_reference = tools.driver.find_element_by_id("customfield_12600")
    topdesk_reference.send_keys(incidentNumber)

    # Submit button
    tools.waitLoadingPageByID("create-issue-submit")
    create_issue_submit = tools.driver.find_element_by_id("create-issue-submit")
    create_issue_submit.click()

def connectToJiraBoard() :
    tools.driver.get("https://jira.atlassian.insim.biz/secure/RapidBoard.jspa?rapidView=464")

def commentButton() :
    tools.waitLoadingPageByID("footer-comment-button")
    create_issue_submit = tools.driver.find_element_by_id("footer-comment-button")
    create_issue_submit.click()

def placeTheTextIntoComment(incidentNumber, incidentTitle) :
    # tools.waitLoadingPageByID("comment")
    # comment = tools.driver.find_element_by_id("comment")

    WebDriverWait(tools.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="mce_0_ifr"]')))
    tools.waitLoadingPageByID("tinymce")
    comment = WebDriverWait(tools.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tinymce"]/p')))
    if (incidentNumber.startswith('I')) :
        comment.send_keys(incidentNumber + " - " + incidentTitle + "\n" + "https://nnbe.topdesk.net/tas/secure/incident?action=lookup&lookup=naam&lookupValue=" + incidentNumber + "\n")
    else :
        comment.send_keys(incidentNumber + " - " + incidentTitle + "\n" + "https://nnbe.topdesk.net/tas/secure/newchange?action=lookup&lookup=number&lookupValue=" + incidentNumber + "\n")
    # Need to exit the iFrame
    tools.driver.switch_to.default_content()

def addComment() :
    tools.waitLoadingPageByID("issue-comment-add-submit")
    create_issue_submit = tools.driver.find_element_by_id("issue-comment-add-submit")
    create_issue_submit.click()
    # add this wait to be sure that the page is loaded correctly before to go to another steps.
    tools.waitLoadingPageByID("footer-comment-button")

