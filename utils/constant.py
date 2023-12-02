import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

EVENT_CODE = "event-002"
MODEL_MAIN= "gpt-3.5-turbo"
MODEL_MEMORY= "text-davinci-002"

SYSTEM_MESSAGE = "write only sentiment of the text (neutral, positive, or negative)"
SUMMARY_MESSAGE = "give summary based on feedback in descriptive way to the event organizer"

FEEDBACKS = {
  "event-001": [
        "The product seems interesting, but I need more information from the Product Launch ABC.",
        "Attended a tech meetup; it was okay, nothing extraordinary.",
        "The updates in the software release were neither impressive nor disappointing.",
        "Moderate turnout at the VR gaming event, some interesting demos.",
        "The panel discussion on future tech trends was balanced, covering pros and cons.",
        "Expected more from the robotics exhibition; felt it lacked innovation.",
        "Exciting innovations and insightful presentations at Tech Conference XYZ!",
        "Impressive strategies discussed for ensuring data protection at the Data Security Workshop.",
        "Incredible talent showcased in the projects at Hackathon 123!",
        "The hands-on workshop on machine learning was fantastic and very informative.",
        "The new features in the latest app update are excellent; loving the improvements!",
        "Concerns raised about the ethical implications of AI technology during the AI Ethics Panel.",
        "Disappointed with the lack of engaging content at the virtual reality meetup.",
        "The software demo was a letdown, not living up to the hype.",
        "The cybersecurity seminar fell short on practical insights; quite dissatisfied.",
        "The environment of technology actually makes me hypes i love the place"
   ],
   "event-002" : [
        "The variety of flavors at this food event is simply incredible! From savory to sweet, there's something to delight every palate.",
        "A culinary extravaganza! The food at this event is not just a treat for the taste buds but also a feast for the eyes. Beautifully presented dishes abound!",
        "I expected more diversity in the food options. The choices seem somewhat limited.",
        "What a delightful fusion of flavors! This event is a celebration of culinary diversity, bringing together the best tastes from around the world.",
        "I'm on a gastronomic journey at this food event. The chefs have truly outdone themselves, turning every bite into a memorable experience.",
        "The atmosphere is as delicious as the food! The live music and vibrant crowd add the perfect seasoning to this already amazing food event.",
        "While the food is good, the organization could be better. Long lines and wait times are a bit frustrating.",
        "Kudos to the organizers for bringing together such a fantastic array of food vendors. I can't decide which booth to visit next – they're all so tempting!",
        "The aroma of spices and the sizzle of grills – this food event is a sensory explosion! I'm enjoying every moment of this culinary adventure.",
        "The food taste sucks, i hate it",
        "Food is not just nourishment; it's an experience. Unfortunately, this event fell short of my expectations. The flavors lacked depth, and the presentation was underwhelming.",
        "The food is good but there is no toilet in there",
        "The place is too small i hate it will not come to this bad place",
        "I love the taste of the cake from the events"
    ]
}
