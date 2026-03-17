from anthropic import Anthropic

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.prompt_engineering.prompt_evaluator import (
    PromptEvaluator,
)
from c1_building_with_claude_api.utils.utils import (
    get_haiku_model,
    add_user_message,
    chat,
    text_from_message,
)


def run_prompt(prompt_inputs: dict):
    client: Anthropic = get_client()
    model: str = get_haiku_model()
    prompt = f"""
    Generate one-day meal plan for an athletes that meets their goal and dietary restrictions.
    
    <athlete_information>
    - Height: {prompt_inputs["height"]}
    - Weight: {prompt_inputs["weight"]}
    - Goal: {prompt_inputs["goal"]}
    - Dietary restrictions: {prompt_inputs["restrictions"]}
    </athlete_information>
    
    Guidelines:
    1. Provide accurate daily calories amount
    2. Display macros: proteins, fats and carbohydrates
    3. Specify the time of the day to eat certain meal
    4. Only use the foods that follows dietary restrictions of the athlete
    5. List each portion size in grams
    6. Keep it budget-friendy if mentioned
    
    Sample with ideal input and output:
    <sample_input>
    height: 180 cm
    weight: 72 kg
    goal: Marathon training - high carbohydrate intake with optimal timing around 2-hour morning run
    restrictions: Vegetarian, no nuts
    </sample_input>
    
    <ideal_output>
    # One-Day Marathon Training Meal Plan
    **Athlete: 180cm, 72kg Vegetarian Runner**
    
    ---
    
    ## Daily Nutrition Summary
    - **Total Calories:** 3,200 kcal
    - **Protein:** 110g (13.75%)
    - **Carbohydrates:** 480g (60%)
    - **Fats:** 85g (26.25%)
    
    *Optimized for 2-hour morning run with strategic carb timing*
    
    ---
    
    ## MEAL PLAN
    
    ### **6:00 AM - Pre-Run Breakfast** ⏰
    *Light, easily digestible carbs*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | White bread | 60g | 160 | 5g | 32g | 1g |
    | Honey | 20g | 61 | 0g | 16g | 0g |
    | Banana | 120g | 107 | 1g | 27g | 0g |
    | **Subtotal** | | **328** | **6g** | **75g** | **1g** |
    
    ---
    
    ### **8:15 AM - During Run** (if needed for 2+ hours)
    *Quick energy boost*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Sports drink (6% carbs) | 500ml | 120 | 0g | 30g | 0g |
    | **Subtotal** | | **120** | **0g** | **30g** | **0g** |
    
    ---
    
    ### **10:30 AM - Post-Run Recovery Meal** ⏰
    *High carbs + protein within 30-45 min of finishing*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Oatmeal (dry) | 60g | 228 | 8g | 41g | 5g |
    | Whole milk | 250ml | 160 | 8g | 12g | 9g |
    | Blueberries | 100g | 57 | 1g | 14g | 0g |
    | Honey | 15g | 46 | 0g | 12g | 0g |
    | **Subtotal** | | **491** | **17g** | **79g** | **14g** |
    
    ---
    
    ### **1:00 PM - Lunch** ⏰
    *Balanced meal with complex carbs*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Brown rice | 150g (cooked) | 195 | 5g | 43g | 2g |
    | Chickpeas | 120g (cooked) | 134 | 7g | 22g | 2g |
    | Spinach | 80g | 22 | 3g | 4g | 0g |
    | Olive oil | 10ml | 90 | 0g | 0g | 10g |
    | Lemon juice | 10ml | 3 | 0g | 1g | 0g |
    | **Subtotal** | | **444** | **15g** | **70g** | **14g** |
    
    ---
    
    ### **3:30 PM - Afternoon Snack** ⏰
    *Energy boost before evening activities*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Whole wheat bread | 50g | 130 | 4g | 24g | 1g |
    | Peanut butter | ❌ *Not allowed* | — | — | — | — |
    | Hummus | 40g | 70 | 3g | 6g | 4g |
    | Carrot sticks | 100g | 41 | 1g | 10g | 0g |
    | Apple | 150g | 81 | 0g | 21g | 0g |
    | **Subtotal** | | **322** | **8g** | **61g** | **5g** |
    
    ---
    
    ### **7:00 PM - Dinner** ⏰
    *Substantial meal with lean protein*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Lentil pasta | 100g (dry) | 360 | 25g | 63g | 2g |
    | Tomato sauce | 150g | 45 | 2g | 8g | 1g |
    | Tofu | 150g | 165 | 20g | 4g | 10g |
    | Broccoli | 120g | 43 | 3g | 8g | 0g |
    | Olive oil | 8ml | 72 | 0g | 0g | 8g |
    | **Subtotal** | | **685** | **50g** | **83g** | **21g** |
    
    ---
    
    ### **9:30 PM - Evening Snack** ⏰
    *Light, sleep-friendly carbs*
    
    | Food | Portion | Calories | Protein | Carbs | Fats |
    |------|---------|----------|---------|-------|------|
    | Greek yogurt (0% fat) | 200g | 130 | 24g | 9g | 0g |
    | Granola (nut-free) | 30g | 120 | 3g | 22g | 3g |
    | Honey | 10g | 31 | 0g | 8g | 0g |
    | **Subtotal** | | **281** | **27g** | **39g** | **3g** |
    
    ---
    
    ## DAILY TOTALS
    | Macronutrient | Amount | % of Calories |
    |---|---|---|
    | **Calories** | **3,251** | — |
    | **Protein** | **123g** | 15% |
    | **Carbohydrates** | **477g** | 59% |
    | **Fats** | **58g** | 16% |
    
    ---
    
    ## 🎯 Key Features for Marathon Training
    
    ✅ **Carb-Loading Strategy:** 59% of calories from carbs (optimal for endurance)  
    ✅ **Pre-Run Fueling:** Simple carbs 1-2 hours before morning run  
    ✅ **Post-Run Recovery:** High carb + protein meal within 45 minutes  
    ✅ **Vegetarian Protein Sources:** Lentils, chickpeas, tofu, Greek yogurt, legume pasta  
    ✅ **No Nuts:** All nut-free alternatives used  
    ✅ **Budget-Friendly:** Uses affordable staples (rice, lentils, oats, beans)  
    ✅ **Hydration:** Include 2-3L water throughout the day
    
    ---
    
    ## 💡 Adjustments
    - **If running longer than 2 hours:** Add 30-60g carbs during run (sports drink, energy gels, or dates)
    - **If weight loss needed:** Reduce to 2,800 kcal by decreasing portion sizes by 15%
    - **If weight gain needed:** Increase to 3,600 kcal by adding extra snacks
    </ideal_output>
    """

    messages = []
    add_user_message(messages, prompt)
    message = chat(client, model, messages)
    return text_from_message(message)


if __name__ == "__main__":
    client: Anthropic = get_client()
    model: str = get_haiku_model()
    evaluator: PromptEvaluator = PromptEvaluator(client, model)
    dataset_path: str = "meal_dataset.json"

    evaluator_extra_criteria: str = """
    Make sure that output should include:
    * daily caloric total, 
    * macro nutrients breakdown, 
    * meals with exact food, portions and timing
    """

    results: list = evaluator.run_evaluation(
        run_prompt, dataset_file=dataset_path, extra_criteria=evaluator_extra_criteria
    )
