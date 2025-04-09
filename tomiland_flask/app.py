from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')


@app.route('/destinations')
def destinations():
    return render_template('destinations.html')


@app.route('/experiences')
def experiences():
    return render_template('experiences.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        experience = request.form.get('experience')
        date = request.form.get('date')

        # You can print to check if it's working
        print(f"Booking from {name} ({email}) for {experience} on {date}")

        return render_template(
            'confirmation.html', 
            name=name, 
            experience=experience, 
            date=date
        )

    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
