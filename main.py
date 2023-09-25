from fastapi import FastAPI
import uvicorn
import os
from app.backend.routers.branch_offices import branch_offices
from app.backend.routers.genders import genders
from app.backend.routers.nationalities import nationalities
from app.backend.routers.pentions import pentions
from app.backend.routers.banks import banks
from app.backend.routers.account_types import account_types
from app.backend.routers.regions import regions
from app.backend.routers.employees import employees
from app.backend.routers.users import users
from app.backend.routers.employee_labor_data import employee_labor_data
from app.backend.routers.employee_extras import employee_extras
from app.backend.routers.alert_types import alert_types
from app.backend.routers.honoraries import honoraries
from app.backend.routers.uniform_types import uniform_types
from app.backend.routers.uniforms import uniforms
from app.backend.routers.segments import segments
from app.backend.routers.job_positions import job_positions
from app.backend.routers.patology_types import patology_types
from app.backend.routers.civil_states import civil_states
from app.backend.routers.document_types import document_types
from app.backend.routers.family_core_data import family_core_data
from app.backend.routers.vacations import vacations
from app.backend.routers.medical_licenses import medical_licenses
from app.backend.routers.rols import rols
from app.backend.routers.news import news
from app.backend.routers.principals import principals
from app.backend.routers.communes import communes
from app.backend.routers.healths import healths
from app.backend.routers.employee_bank_accounts import employee_bank_accounts
from app.backend.routers.documents_employees import documents_employees
from app.backend.routers.contract_data import contract_data
from app.backend.routers.contract_types import contract_types
from app.backend.routers.medical_license_types import medical_license_types
from app.backend.auth.login_users import login_users
from app.backend.routers.clock_users import clock_users
from app.backend.routers.budgets import budgets
from app.backend.routers.collections import collections
from app.backend.routers.dtes import dtes
from app.backend.routers.letter_types import letter_types
from app.backend.routers.end_documents import end_documents
from app.backend.routers.mesh_data import mesh_data
from app.backend.routers.kardex_data import kardex_data
from app.backend.routers.honorary_reasons import honorary_reasons
from fastapi.middleware.cors import CORSMiddleware
from app.backend.routers.progressive_vacations import progressive_vacations
from app.backend.routers.employee_types import employee_types
from app.backend.routers.regimes import regimes
from app.backend.routers.salary_settlements import salary_settlements
from app.backend.routers.document_managements import document_managements

app = FastAPI()

os.environ['SECRET_KEY'] = '7de4c36b48fce8dcb3a4bb527ba62d789ebf3d3a7582472ee49d430b01a7f868'
os.environ['ALGORITHM'] = 'HS256'

# Configura las opciones de CORS
origins = ["*"]

# Agrega el middleware de CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(branch_offices)
app.include_router(genders)
app.include_router(nationalities)
app.include_router(pentions)
app.include_router(banks)
app.include_router(account_types)
app.include_router(regions)
app.include_router(employees)
app.include_router(users)
app.include_router(employee_labor_data)
app.include_router(employee_extras)
app.include_router(alert_types)
app.include_router(honoraries)
app.include_router(uniform_types)
app.include_router(uniforms)
app.include_router(segments)
app.include_router(job_positions)
app.include_router(patology_types)
app.include_router(civil_states)
app.include_router(document_types)
app.include_router(family_core_data)
app.include_router(vacations)
app.include_router(medical_licenses)
app.include_router(rols)
app.include_router(news)
app.include_router(principals)
app.include_router(communes)
app.include_router(healths)
app.include_router(employee_bank_accounts)
app.include_router(documents_employees)
app.include_router(contract_data)
app.include_router(contract_types)
app.include_router(medical_license_types)
app.include_router(login_users)
app.include_router(clock_users)
app.include_router(budgets)
app.include_router(collections)
app.include_router(dtes)
app.include_router(letter_types)
app.include_router(end_documents)
app.include_router(mesh_data)
app.include_router(kardex_data)
app.include_router(honorary_reasons)
app.include_router(progressive_vacations)
app.include_router(employee_types)
app.include_router(regimes)
app.include_router(salary_settlements)
app.include_router(document_managements)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)