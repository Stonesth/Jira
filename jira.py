import os
import re # regular expression

from Tools import tools_v000 as tools
from os.path import dirname
from datetime import datetime
from selenium.webdriver.common.keys import Keys

# -4 for the name of this project Jira
save_path = dirname(__file__)[ : -4]
propertiesFolder_path = save_path + "Properties"

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

def connectToJira(jira) :
    tools.driver.get("https://jira.atlassian.insim.biz/browse/" + jira)

def recoverJiraInformation() :
    
    # jiraTitle
    global jiraTitle
    tools.waitLoadingPageByID("summary-val")
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
    description_text = tools.driver.find_element_by_id("description-val").text
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

def createFolderJira(jira) :
    os.mkdir(save_path + jira)

def createFileInto(jira, jiraTitle, description_text) :
    name_of_file = jira + "_Comment_v001"
    completeName = os.path.join(save_path + jira, name_of_file+".txt")   
    file1 = open(completeName, "w")

    file1.write("\n")    
    file1.write("========================================================================================================================"+"\n")
    file1.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    file1.write("\n")
    file1.write(jiraTitle.encode('utf-8').strip() + "\n")
    file1.write("\n")
    file1.write(description_text + "\n")
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
    
    tools.waitLoadingPageByID("action_id_51")
    workflow = tools.driver.find_element_by_id("action_id_51")
    workflow.click()

def selectJira() :
    tools.driver.get("https://jira.atlassian.insim.biz/secure/RapidBoard.jspa?rapidView=464&quickFilter=1705")    
    
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


def createJira(jiraTitle, description_text, incidentNumber) :
    tools.waitLoadingPageByID("create_link")
    create_link = tools.driver.find_element_by_id("create_link")
    create_link.click()

    # click to select incident
    tools.waitLoadingPageByID("issuetype-field")
    issuetype_field = tools.driver.find_element_by_id("issuetype-field")
    issuetype_field.click()
    issuetype_field.send_keys("Incident")
    issuetype_field.send_keys(Keys.ENTER)

    # summary
    tools.waitLoadingPageByID("summary")
    summary = tools.driver.find_element_by_id("summary")
    summary.send_keys(jiraTitle)

    # description
    tools.waitLoadingPageByID("description")
    description = tools.driver.find_element_by_id("description")
    description.send_keys(incidentNumber + "\n")
    description.send_keys("https://nnbe.topdesk.net/tas/secure/incident?action=lookup&lookup=naam&lookupValue=" + incidentNumber + "\n")

    # assign to me
    tools.waitLoadingPageByID("assign-to-me-trigger")
    assign_to_me_trigger = tools.driver.find_element_by_id("assign-to-me-trigger")
    assign_to_me_trigger.click()

    # Need to go down of the page
    tools.waitLoadingPageByID("description")
    description = tools.driver.find_element_by_id("description")
    description.send_keys(Keys.PAGE_DOWN)

    # sprint
    tools.waitLoadingPageByID("customfield_10007-field")
    customfield_10007 = tools.driver.find_element_by_id("customfield_10007-field")
    customfield_10007.send_keys(sprint)
    customfield_10007.send_keys(Keys.ENTER)

    # Need to go Up of the page
    tools.waitLoadingPageByID("description")
    description = tools.driver.find_element_by_id("description")
    description.send_keys(Keys.PAGE_UP)

    # --------------------- Link ----------------------
    tools.waitLoadingPageByXPATH("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[2]/a/strong")
    link_button = tools.driver.find_element_by_xpath("/html/body/div[8]/div[2]/div[1]/div/form/div[1]/div[2]/div/ul/li[2]/a/strong")
    link_button.click()

    # Epic Link
    tools.waitLoadingPageByID("customfield_10008-field")
    customfield_10008 = tools.driver.find_element_by_id("customfield_10008-field")
    customfield_10008.click()
    customfield_10008.send_keys(epic_link)    
    customfield_10008.send_keys(Keys.ARROW_DOWN)    
    customfield_10008.send_keys(Keys.ENTER)    

    # Labels
    tools.waitLoadingPageByID("labels-textarea")
    labels_textarea = tools.driver.find_element_by_id("labels-textarea")
    labels_textarea.send_keys("IT4IT")
    labels_textarea.send_keys(Keys.ENTER)
    
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