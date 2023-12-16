import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv

# Load OpenAI Key
load_dotenv()

# Call LLM
def getLLMResponse(query, age_option, tasktype_option):
    llm = OpenAI(temperature=.9, model="gpt-3.5-turbo-instruct") 

    if age_option == 'Kid':
        examples = [
            {
                "query": "What is a mobile?",
                "answer": " A mobile is a magical device that fits in your pocket, like a mini enchanted playground. It has games, videos and talking pictures, but be careful, it can turn on and play music for you."
            },

            {
                "query": " What are your dreams?",
                "answer": "My dreams are like colorful adventures, where I become a superhero and save the day! I dream of giggles, ice cream parties and having a pet dragon named Sparkles..."
            },

            {
                "query": " What are your ambitions?",
                "answer": "I want to be a super funny comedian, spread laughter everyhwere I go. I also want to be a master cook & cook candy all day"
            },
            {
                "query": " How much do you love your dad?",
                "answer": "I love my dad to the moon and back, with sprinkles and unicorns on top. He's my super hero."
            }
        ]

        elif age_option == "Adult":
             examples = [
            {
                "query": "What is a smartphone?",
                "answer": "A smartphone is a sophisticated handheld electronic device that goes beyond mere communication. It serves as a multifunctional tool, seamlessly integrating features such as advanced computing, high-quality photography, internet browsing, and a myriad of applications for productivity and entertainment. Essentially, it's a portable powerhouse that connects you to the world while fitting in the palm of your hand."
            },

            
        ]

         elif age_option == "Senior Citizen":
             examples = [
            {
               
                "query": "What is a cellphone?",
                "answer": "A cellphone, dear friend, is a marvelous invention that allows you to make calls, send messages, and stay connected with your loved ones. It's like a tiny, portable telephone that you can carry in your pocket or purse. Some even have larger buttons and simpler menus to make it easier for you to use. Think of it as a modern version of the good old telephone, but with a touch of technology magic to keep you in touch with the world around you."
            },


        ]


    example_template = """
    Question {query}
    Response {answer}
    """

    example_prompt = PromptTemplate(input_variables=["query", "answer"], template=example_template)

    prefix = """
    You are a {template_age_option} and {template_tasktype_option}:
    Here are some few examples
    """

    suffix = """
    Question: {template_userInput}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )

    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["template_userInput", "template_age_option", "template_tasktype_option"],
        example_separator="\n"
    )

    print(new_prompt_template.format(template_userInput=query, template_age_option = age_option, template_tasktype_option=tasktype_option))
    response = llm(new_prompt_template.format(template_userInput=query, template_age_option = age_option, template_tasktype_option=tasktype_option))

    print(response)

    return response


#UI STARTS HERE

st.set_page_config(page_title="Marketing Tool", page_icon=':robot:', layout='centered', initial_sidebar_state='collapsed')

st.header('Hey, how can I help you?')

form_input = st.text_area('Enter text', height=275)

tasktype_option = st.selectbox(
    ('Please select the action to be performed'),
    ('Write a sales copy', 'Create a tweet', 'Write a product description'),
    key=1
)

age_option = st.selectbox('For which age group?', ('Kid', 'Adult', 'Senior Citizen'), key=2)
numberOfWords = st.slider('Words limit', 1, 200, 25)
submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input, age_option, tasktype_option))

#UI ENDS HERE




