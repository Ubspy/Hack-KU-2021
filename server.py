from flask import Flask, session, render_template, request
import prompt
import nlp

app = Flask(__name__)
app.secret_key = b'\xf0E\x18\x0bx0\xb9y\xc6\xc9\xdaA\x8e/\xabH' # super secret

@app.route("/")
def index():
    # always create a new session (meaning clear data from old session)
    session['prompt'] = 'start'
    return render_template('webpage.html')

@app.route("/message", methods=['POST'])
def test():
    tmp = getResponse(request.form['message'])
    return(tmp)

def getResponse(user_message):
    user_in = user_message[0:-1].lower() # slice to cut out the newline character
    words = user_in.split(" ")
    choice = None
    p = prompt.get_obj(session['prompt']) # the current prompt object
    
    if p.generated:
        choice = p.next_name(' ') # A space is default if there's no branching to be done
        session['prompt'] = choice # Saves this value to use in the next iteration
        p = prompt.get_obj(choice) # Gets next prompt message

        # Set up NLP to generate response
        generator = nlp.NLPResponse()

        # Return dictionary of generated response, then the pre-done response
        return {'generatedMessage': generator.give_reply(user_message), 'nextMessage': p.message}
    else:
        for word in words:
            choice = p.next_name(word)
            if (choice is not None):
                break
        if (choice is None):
            return("Sorry, I didn't understand that. " + p.message)
        else:
            session['prompt'] = choice # p = next value based on user input
            p = prompt.get_obj(choice)
            return(p.message)

if __name__ == "__main__":
    app.run()