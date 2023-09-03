import json
from uuid import uuid4
from sqlalchemy.orm import Session
from api.chat.home import generate_home_design_response
from api.chat.business import generate_bunisess_design_response
from api.common import models
from api.common.schemas import HomeCreate, HomeUpdate, BusinessCreate


async def create_business_home(db: Session, home: BusinessCreate, user_id: str = None):
    if home.type != "business":
        return None   
    
    user_ansewr = {
        "question1": home.question1,
        "question2": home.question2,
        "question3": home.question3,
        "question4": home.question4,
        "question5": home.question5,
        "question6": home.question6,
        "question7": home.question7,
        "question8": home.question8,
        "question9": home.question9,
        "question10": home.question10,
        "question11": home.question11,
        "question12": home.question12,
        "question13": home.question13, 
        "question14": home.question14,
        "question15": home.question15,
        
    }
    
    respose = generate_bunisess_design_response(user_ansewr) 
    if respose is None:
        return None
    db_home = models.Home(
        id=str(uuid4()),
        title=home.title,
        home_type=home.type,
        user_id=user_id,
        data=json.dumps(respose[0]),
        context=json.dumps(respose[1]),
    )
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home.toJSON()

async def create_home(db: Session, home: HomeCreate, user_id: str = None):
    
    
    if home.type != "home":
        return None
    
    user_ansewr = {
        "question1": home.question1,
        "question2": home.question2,
        "question3": home.question3,
        "question4": home.question4,
        "question5": home.question5,
        "question6": home.question6,
        "question7": home.question7,
        "question8": home.question8,
        "question9": home.question9,
        "question10": home.question10,
        "question11": home.question11,
        "question12": home.question12,
        "question13": home.question13, 
        "question14": home.question14
        
    }
        
    respose = generate_home_design_response(user_ansewr)
    
    if respose is None:
        return None
    db_home = models.Home(
        id=str(uuid4()),
        title=home.title,
        home_type=home.type,
        user_id=user_id,
        data=json.dumps(respose[0]),
        context=json.dumps(respose[1]),
    )
    db.add(db_home)
    db.commit()
    db.refresh(db_home)
    return db_home.toJSON()

async def get_home(db: Session, home_id: str):
    result = db.query(models.Home).filter(models.Home.id == home_id).first()
    if result is None:
        return None
    return result.toJSON()

async def get_homes(db: Session, skip: int = 0, limit: int = 100, user_id: str = None):
    return db.query(models.Home).filter(models.Home.user_id == user_id).offset(skip).limit(limit).all()

async def update_home(db: Session, home: HomeUpdate, home_id: str):
    user_ansewr = {
        "question1": home.question1,
        "question2": home.question2,
        "question3": home.question3,
        "question4": home.question4,
        "question5": home.question5,
        "question6": home.question6,
        "question7": home.question7,
        "question8": home.question8,
        "question9": home.question9,
        "question10": home.question10,
        "question11": home.question11,
        "question12": home.question12,
        "question13": home.question13, 
        "question14": home.question14

        
    }
    db_home = db.query(models.Home).filter(models.Home.id == home_id).first()
    response = generate_home_design_response(user_ansewr)
    if response is None:
        return None
    db_home.title = home.title
    db_home.data = json.dumps(response[0])
    db_home.context = json.dumps(response[1])
    db.commit()
    db.refresh(db_home)
    return db_home.toJSON()

async def update_business_home(db: Session, home: BusinessCreate, home_id: str):
    user_ansewr = {
        "question1": home.question1,
        "question2": home.question2,
        "question3": home.question3,
        "question4": home.question4,
        "question5": home.question5,
        "question6": home.question6,
        "question7": home.question7,
        "question8": home.question8,
        "question9": home.question9,
        "question10": home.question10,
        "question11": home.question11,
        "question12": home.question12,
        "question13": home.question13, 
        "question14": home.question14,
        "question15": home.question15,
        
    }
    db_home = db.query(models.Home).filter(models.Home.id == home_id).first()
    response = generate_bunisess_design_response(user_ansewr)
    if response is None:
        return None
    db_home.title = home.title
    db_home.data = json.dumps(response[0])
    db_home.context = json.dumps(response[1])
    db.commit()
    db.refresh(db_home)
    return db_home.toJSON()

async def delete_home(db: Session, home_id: str):
    db_home = db.query(models.Home).filter(models.Home.id == home_id).first()
    db.delete(db_home)
    db.commit()
    return db_home.toJSON()

def generate_home_project_summary(project):
    data = json.loads(project['data'])
    title = project['title']
    feasibility = "feasibile" if data['feasibility'] else "not feasible"
    home_appearance = data['home_appearance']
    budget_analysis = data['budget_analysis']
    timeline_analysis = data['timeline_analysis']
    recommendations = data['recommendations']

    summary = f"Design: {title} (Home)\n"
    summary += f"This home design is deemed {feasibility}. It features an interior style of {home_appearance['interior_style']} and an exterior style of {home_appearance['exterior_style']} with a color palette in {home_appearance['color_palette']} tones. The architectural design incorporates {home_appearance['architectural_features']} elements. The property boasts {home_appearance['numberOfclass']} bedrooms and {home_appearance['numberOffloor']} floors, offering a cozy and inviting atmosphere.\n"
    summary += f"The estimated budget for this project is {budget_analysis['estimated_budget']}. The budget allocation includes {', '.join(budget_analysis['budget_allocation'])}. To align with the budget, it is suggested to {budget_analysis['suggested_changes']}.\n"
    summary += f"The project is expected to be completed in {timeline_analysis['estimated_timeline']} and is divided into {len(timeline_analysis['phasing_details']['phases'])} phases. Additionally, the project comes with the following recommendations: {', '.join(recommendations)}."

    return summary

def generate_business_project_summary(project):
    data = json.loads(project['data'])
    title = project['title']
    feasibility = "feasibile" if data['feasibility'] else "not feasible"
    building_details = data['building_details']
    occupancy_details = data['occupancy_details']
    design_preferences = data['design_preferences']
    construction_and_timing = data['construction_and_timing']
    budget_analysis = data['budget_analysis']
    timeline_analysis = data['timeline_analysis']
    recommendations = data['recommendations']

    summary = f"Design: {title} Business\n"
    summary += f"This business project is considered {feasibility}. It serves as office space with a total square footage of {building_details['total_square_footage']}. The architectural style is {building_details['architectural_style']} with {building_details['number_of_floors']} floors. Local authorities' approval is required due to zoning constraints.\n"
    summary += f"The project is designed to accommodate {occupancy_details['number_of_occupants']} occupants with a mix of specialized and standard spaces. It provides basic accessibility features, amenities, and sufficient parking for employees and visitors.\n"
    summary += f"The design preferences emphasize a contemporary and open ambiance, drawing inspiration from {', '.join(design_preferences['design_inspirations'])}. Advanced technology integration for security, access control, and energy management is planned.\n"
    summary += f"The project faces weather-related challenges, including {construction_and_timing['weather_site_challenges']}, and a phased construction approach with partial occupancy is feasible. The estimated budget is {budget_analysis['estimated_budget']}, with suggested cost-saving measures.\n"
    summary += f"The project is expected to take {timeline_analysis['estimated_timeline']} to complete, divided into {len(timeline_analysis['phasing_details']['phases'])} phases. Recommendations include {', '.join(recommendations)}."

    return summary

async def get_home_summary(db: Session, home_id: str):
    db_home = db.query(models.Home).filter(models.Home.id == home_id).first()
    if db_home is None:
        return None
    if db_home.home_type == "home":
        return generate_home_project_summary(db_home.toJSON())
    elif db_home.home_type == "business":
        return generate_business_project_summary(db_home.toJSON())
    else:
        return None
    
def generate_prompt_for_image(project):
    data = json.loads(project['data'])
    project_type = "home" if project['home_type'] == "residential home" else "Office Space or Business"
    home_appearance = data.get('home_appearance', None)
    building_details = data.get('building_details', None)

    summary = f"Design a building for a client. The client is looking for a {project_type} design. The client has provided the following information:\n"
    
    if home_appearance:
        summary += f"It features an interior style of {home_appearance['interior_style']} and an exterior style of {home_appearance['exterior_style']} with a color palette in {home_appearance['color_palette']} tones. The architectural design incorporates {home_appearance['architectural_features']} elements. The property boasts {home_appearance['numberOfclass']} bedrooms and {home_appearance['numberOffloor']} floors, offering a cozy and inviting atmosphere."
    
    if building_details:
        summary += f"It serves as {building_details['building_purpose']} with a total square footage of {building_details['total_square_footage']}. The architectural style is {building_details['architectural_style']} with {building_details['number_of_floors']} floors. Local authorities' approval is required due to zoning constraints."
    
    return summary


