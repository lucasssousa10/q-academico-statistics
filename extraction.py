from selenium import webdriver
import time
import json

##
username = ""
password = ""

course_id = "23103 - Técnico Integrado em Informática"
periodo = "1"
class_code = "20191.23103.1A"
part = "N2"
##

driver = webdriver.Firefox(executable_path='/home/lucas/development/webdrivers/geckodriver')
driver.get("https://qacademico.ifce.edu.br")

time.sleep(1)

# login as professor
element = driver.find_elements_by_class_name("item_login_pagina_inicial")[0]
element.click()

time.sleep(1)

# login form

element_login = driver.find_element_by_name("LOGIN")
element_passw = driver.find_element_by_name("SENHA")
element_btnok = driver.find_element_by_id("btnOk")

element_login.send_keys(username)
element_passw.send_keys(password)

element_btnok.click()

time.sleep(1)

# open the students by class map

driver.get("https://qacademico.ifce.edu.br/qacademico/index.asp?t=3086");
time.sleep(1)

#filter by 

name_field = driver.find_element_by_name("COD_CURSO")
for opt in name_field.find_elements_by_tag_name("option"):
    if opt.text == course_id:
        opt.click()
        break

time.sleep(1)

peri_field = driver.find_element_by_name("PERIODO")
for opt in peri_field.find_elements_by_tag_name("option"):
    if opt.text == periodo:
        opt.click()
        break

time.sleep(1)

cod_class_fld = driver.find_element_by_name("COD_TURMA")
for opt in cod_class_fld.find_elements_by_tag_name("option"):
    if opt.text == class_code:
        opt.click()
        break

time.sleep(1)

cod_class_fld = driver.find_element_by_name("N_ETAPA")
for opt in cod_class_fld.find_elements_by_tag_name("option"):
    if opt.text == part:
        opt.click()
        break

#extract disc

table_disc = driver.find_element_by_css_selector("body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > p:nth-child(5) > table:nth-child(1)")
discs = table_disc.find_elements_by_class_name("conteudoTexto")

disciplinas = {}
for row in discs:
    disciplinas[row.text.split(" - ")[0]] = {"nome": row.text.split(" - ")[1], "alunos": []}

#extrai dados das disciplinas
disc_order = driver.find_element_by_css_selector("body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1)")
disc_order = disc_order.find_elements_by_class_name("rotulo")

arr_disc = []
for disc in disc_order:
    arr_disc.append(disc.text)

ch_total = driver.find_element_by_css_selector("tr.rotulo:nth-child(2)")
ch_total = ch_total.find_elements_by_class_name("rotulo")

i = 0
for ch in ch_total:
    disciplinas[arr_disc[i]]["ch_total"] = int(ch.text)
    i = i + 1

ch_min = driver.find_element_by_css_selector("tr.rotulo:nth-child(3)")
ch_min = ch_min.find_elements_by_class_name("rotulo")

i = 0
for ch in ch_min:
    disciplinas[arr_disc[i]]["ch_min"] = int(ch.text)
    i = i + 1

#extrai dados do alunos

table_disc = driver.find_element_by_css_selector("body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > table:nth-child(4)")
rows_students = table_disc.find_elements_by_tag_name("tr")

i = 0
for row in rows_students:
    if i > 4 and i % 2 != 0:
        cols = row.find_elements_by_tag_name("td")
        matricula = cols[0].text
        nome_aluno = cols[1].text

        j = 2 #controle de coluna
        d = 0 #id disciplina
        while j < len(cols) - 1:
            key = arr_disc[d]

            nota = cols[j].text
            if nota == "-" or nota == " ":
                nota = "0.0"
            nota = float(nota)

            faltas = cols[j + 1].text
            if faltas == "-" or faltas == " ":
                faltas = "0"
            faltas = int(faltas)
            
            sit = cols[j + 2].text
            if sit == "-" or sit == " ":
                sit = "Sem Inf."
            
            disciplinas[key]["alunos"].append({
                "matricula": matricula,
                "nome": nome_aluno,
                "nota": nota,
                "faltas": faltas,
                "situacao": sit
            })

            d = d + 1
            j = j + 3
    i = i + 1

driver.close()
filename="extractions/{}_{}.json".format(class_code, part)
with open(filename, 'w') as json_file:
  json.dump(disciplinas, json_file)