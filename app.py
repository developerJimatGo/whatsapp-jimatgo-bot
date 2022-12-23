from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://jimatgo:jimatgo123@cluster0.mzfin1z.mongodb.net/?retryWrites=true&w=majority")
db = cluster["jimatgo"]
users = db["users"]
inquiries = db["inquiries"]

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def reply():

    text = request.form.get("Body")
    number = request.form.get("From")
    res = MessagingResponse()
    user = users.find_one({"number": number})

    if not bool(user):  # first-time user
        res.message("Hi, welcome to *JimatGo*, the best *quick service center* in your neighborhood. \n\n"
                          "You can choose from one of the options below: \n\n"
                          "Type\n"
                          "\n1️⃣ for FAQs\n"
                          "2️⃣ for Tyre Balance & Align Package\n"
                          "3️⃣ for Aircond Flushing \n"
                          "4️⃣ for Service Provided\n"
                          "5️⃣ for Partner Workshop\n"
                          "6️⃣ for Book/Further Inquiries\n"
                          "7️⃣ for Live Agent\n")
        users.insert_one({"number": number, "status": "main", "messages": []})

    elif user["status"] == "main":
        try:
            option = text
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == "JimatGo":
            res.message("Thanks for approaching us again! 😇"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
        elif option == "1":
            res.message("Glad that you are interested to know more! 😉\nFeel free to know more about us anytime.\n\nType\n\n 1️⃣ for About Us\n 2️⃣ for Operating Hours\n 3️⃣ for Our Location\n 0️⃣0️⃣ to Return to Main Menu")
            users.update_one({"number": number}, {"$set": {"status": "FAQ"}})

        elif option == "2":
            res.message("Steering wheel-off center? Feeling some vibrations? Tyre unevenly worn off? Noisy tyres? It's never too late to balance and align your tyre for a safety driving experience. 🔧\n\nFor just only RM199-299 you can enjoy up to 6 times of tyre balancing and alignment for a year\n\nEveryone deserves a better driving experiences, subscribe and enjoy it now at our partner workshop! 😀\n\nSubscribe & T&C here:\nhttps//www.verygoodexamples.com/pleasebuytheabpackageiloveyougaogao\n\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_main"}})  # updated
        elif option == "3":
            res.message("Miss the cool breeze from your AC of your car in a hot sunny days? Join our membership to enjoy cooler & cleaner driving experiences. 💨\n\nWith RM100 a year, you can enjoy:\n✅ AC Flushing Services with RM5 (Market Price is RM180)\n✅ Essential Fluids Replacement for every 40000km milage with RM0 (Market Price is RM3XX)\n\nEveryone deserves a comfortable driving experiences, subscribe and enjoy it now at our partner workshop! 😀\n\nSubscribe & T&C here:\n https//www.verygoodexamples.com/pleasebuytheabpackageiloveyougaogao2 \n\n0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_main"}})  # updated
        elif option == "4":
            res.message("Regular maintainance keeps car breakdown away, we JimatGo provide regular lite service & maintainance for your lovely car. 💕\n\nQuality Services we provide 🌟:\n\n*Engine & Filter Services*\n✅ Replace Fully/Semi Engine Oil & Oil Filter\n✅ Replace Air Filter\n✅ Replace Cabin Filter\n\n*Brake Services*\n✅ Replace Break Pads\n✅ Replace Break Disc\n✅ Replace Break Fluid\n\n*Fluids Replace/Refill*\n✅ Coolant\n✅ Transmission Fluid\n✅ Brake Fluid\n✅ Power Steering Fluid\n✅ Gearbox Fluid\n\n*Other*\n✅ Replace Spark Plug\n✅ Replace Car Battery\n\nTo book an appointment or check for more details information, type:\n\n 9️⃣ for Book/Further Inquiries\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "services"}})
        elif option == "5":
            res.message("We, JimatGo, collaborate with a few partner workshops to carry out more comprehensive services and benefits for our lovely users.😊\n\nTo date, we have our partner workshops throughout Klang Valley area including Semenyih, Puchong, Kepong area. We choose our partners wisely just to ensure our users enjoy up-to-par services.\n\nOur partners list here:\nhttps//www.verygoodexamples.com/pleasebuytheabpackageiloveyougaogao3\n\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_main"}})  # updated
        elif option == "6":
            res.message("Please provide us with some information for us to serve you better, our agent will be here shortly to chat with you 😉\n\nTo make appointment or not sure what happen to your car, we would like to invite you to our workshops to enjoy FOC inspection!\n\n 0️⃣0️⃣ to Return to Menu")
            res.message("*Name:*\n*Postcode:*\n*Car Plate:*\n*Brand, Model, Year:*\n*Mileage:*\n*Intended Service/Package:*\n*Chassis/Vehicle Registration No (if able):*\n\n*Prefered Date:*\n*Prefered Time:*")
            users.update_one({"number": number}, {"$set": {"status": "inquiries"}})
        elif option == "7":  # updated
            res.message("Please hold while we connect you to our next available agent, thanks for your patience.\n\nOur live chat agents are usually active from Mon to Fri 9 pm to 6 pm, you may also approach them via *Whatsapp: www.pleasedontwhatsappme.com.* 😊\n\nType 0️⃣0️⃣ to Cancel Request")
            users.update_one({"number": number}, {"$set": {"status": "return_to_main_CancelAgentRequest"}})
        else:
            res.message("Please enter a valid response")
            
    elif user["status"] == "FAQ":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Thanks for approaching us again! 😇\n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        elif option == 1:
            res.message("Collaborating with shopping malls and workshops, JimatGo is the best quick car service platform in your neighborhood.😉\n\nStarting from Malaysia, we aim to provide;\n✅ Affordable Price\n✅ Genuine Quality\n✅ Transparent Service\n✅ Nationwide Warranty\n\nWith *JimatGo*, we save you the time and hassle.\n\n 0️⃣ to Return to FAQ\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_FAQ"}})  # updated
        elif option == 2:
            res.message("Our operating hours are *Monday - Sunday, 10am - 8pm*, while our partners workshop are usually *Monday - Saturday, 9am - 7pm*. 😉\nKindly drop us your inquiry for more information and start enjoying quick and affordable services with us. We can wait to see you!\n\n 0️⃣ to Return to FAQ\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_FAQ"}})  # updated
        elif option == 3:
            res.message("Our JimatGo outlet is located at Lotus's Kepong Village Mall. Interested? Just pick one link and you are good to go!\n\n🗺️ https://maps.app.goo.gl/nJsRbxzFbiNHHaLe8\n🗺️ https://waze.com/ul/hw2860trsg\n\nOur partners workshops are also located at Semenyih and Puchong too! For more information, type ""1"". \n\n\n 0️⃣ to Return to FAQ\n 1️⃣ for Partner Workshop\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "location"}})

        else:
            res.message("Please enter a valid response")

    elif user["status"] == "return_to_FAQ":  # let user enter only "00" to return main menu and "0" to return FAQ
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Thanks for approaching us again! 😇\n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        elif option == 0:
            res.message("Glad that you are interested to know more! 😉\nFeel free to know more about us anytime.\n\nType\n\n 1️⃣ for About Us\n 2️⃣ for Operating Hours\n 3️⃣ for Our Location\n 0️⃣0️⃣ to Return to Main Menu")
            users.update_one({"number": number}, {"$set": {"status": "FAQ"}})

        else:
            res.message("Please enter a valid response")

    elif user["status"] == "location":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Thanks for approaching us again! 😇 \n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        # elif option == 0:  // since back to main menu only this one no need
        #    res.message("Glad that you are interested to know more! 😉\nFeel free to know more about us anytime.\n\nType\n\n 1️⃣ for About Us\n 2️⃣ for Operating Hours\n 3️⃣ for Our Location\n 0️⃣0️⃣ to Return to Main Menu")
        #    users.update_one({"number": number}, {"$set": {"status": "FAQ"}})

        elif option == 1:  # updated
            res.message("We, JimatGo, collaborate with a few partner workshops to provide more comprehensive services and benefits for our lovely users.😊\n\n"
                        "We have partner workshops throughout the Klang Valley area, including Semenyih, Puchong, and Kepong. We choose our partners wisely to "
                        "ensure our users enjoy up-to-par services.\n\n"
                        "Our partners' list here:\n\nhttps//www.verygoodexamples.com/pleasebuytheabpackageiloveyougaogao3\n\n 0️⃣0️⃣ to Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "return_to_main"}})
        else:
            res.message("Please enter a valid response")

    elif user["status"] == "return_to_main":  # let user enter only "00" to return main menu
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Thanks for approaching us again! 😇 \n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        else:
            res.message("Please enter a valid response")

    elif user["status"] == "return_to_main_CancelAgentRequest":  # let user enter only "00" to cancel live agent request
        # inquiries.delete_one({"number": number, "status": "booked_inquiries"}) - used to delete inquiries
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Your request has been cancelled. If there is anything else that we can help you with, just enter 0️⃣0️⃣ ")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        else:
            res.message("Please enter a valid response")

    elif user["status"] == "services":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if text == "00":
            res.message("Thanks for approaching us again! 😇 \n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        elif option == 9:
            res.message("Please provide us with some information for us to serve you better, our agent will be here shortly to chat with you 😉\n\nTo make appointment or not sure what happen to your car, we would like to invite you to our workshops to enjoy FOC inspection!\n\n 0️⃣0️⃣ to Return to Menu")
            res.message("*Name:*\n*Postcode:*\n*Car Plate:*\n*Brand, Model, Year:*\n*Mileage:*\n*Intended Service/Package:*\n*Chassis/Vehicle Registration No (if able):*\n\n*Prefered Date:*\n*Prefered Time:*")
            users.update_one({"number": number}, {"$set": {"status": "inquiries"}})

        else:
            res.message("Please enter a valid response")

    elif user["status"] == "inquiries":  # updated (first booking)

        if text == "00":
            res.message("Thanks for approaching us again! 😇 \n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        elif len(text) > 30:
            inquiries.insert_one(
                {"number": number, "status": "booked_inquiries", "booking": text, "order_time": datetime.now()})
            res.message("*Inquiry received and being processed*😊, please hold while we connect you to the next available agent.\n\n1️⃣ to Book another Inquiry\n0️⃣0️⃣ to Cancel and Return to Menu")
            users.update_one({"number": number}, {"$set": {"status": "inquiries_another_booking"}})

        else:
            res.message("Please enter a valid response")
            users.update_one({"number": number}, {"$set": {"status": "inquiries"}})
         #   res.message("Please provide proper information for inquires/booking")
         #   res.message("*Name:*\n*Postcode:*\n*Car Plate:*\n*Brand, Model, Year:*\n*Mileage:*\n*Intended Service/Package:*\n*Chassis/Vehicle Registration No (if able):*\n\n*Prefered Date:*\n*Prefered Time:*")
         #   res.message("\n\n 0️⃣0️⃣ to Return to Menu")
         #   users.update_one({"number": number}, {"$set": {"status": "inquiries"}})

    elif user["status"] == "inquiries_another_booking":  # updated (another booking)

        if text == "00":
            res.message("Thanks for approaching us again! 😇 \n\n"
                        "You can choose from one of the options below: \n\n"
                        "Type\n"
                        "\n1️⃣ for FAQs\n"
                        "2️⃣ for Tyre Balance & Align Package\n"
                        "3️⃣ for Aircond Flushing \n"
                        "4️⃣ for Service Provided\n"
                        "5️⃣ for Partner Workshop\n"
                        "6️⃣ for Book/Further Inquiries\n"
                        "7️⃣ for Live Agent\n")
            users.update_one({"number": number}, {"$set": {"status": "main"}})

        elif text == "1":
          # inquiries.insert_one({"number": number, "status": "booked_inquiries", "booking": text, "order_time": datetime.now()})
            res.message("*Name:*\n*Postcode:*\n*Car Plate:*\n*Brand, Model, Year:*\n*Mileage:*\n*Intended Service/Package:*\n*Chassis/Vehicle Registration No (if able):*\n\n*Prefered Date:*\n*Prefered Time:*")
            users.update_one({"number": number}, {"$set": {"status": "inquiries_another_booking"}})

        elif len(text) > 30:
            res.message("*Inquiry received and being processed*😊, please hold while we connect you to the next available agent.\n\n1️⃣ to Book another Inquiry\n0️⃣0️⃣ to Cancel and Return to Menu")
            inquiries.insert_one({"number": number, "status": "booked_inquiries", "booking": text, "order_time": datetime.now()})
            users.update_one({"number": number}, {"$set": {"status": "inquiries_another_booking"}})

        else:
            res.message("Please enter a valid response")
            users.update_one({"number": number}, {"$set": {"status": "inquiries_another_booking"}})
         #   res.message("Please provide proper information for inquires/booking")
         #   res.message("*Name:*\n*Postcode:*\n*Car Plate:*\n*Brand, Model, Year:*\n*Mileage:*\n*Intended Service/Package:*\n*Chassis/Vehicle Registration No (if able):*\n\n*Prefered Date:*\n*Prefered Time:*")
         #   res.message("\n\n 0️⃣0️⃣ to Return to Menu")
         #   users.update_one({"number": number}, {"$set": {"status": "inquiries"}})
    return str(res)


if __name__ == "__main__":
    app.run()
