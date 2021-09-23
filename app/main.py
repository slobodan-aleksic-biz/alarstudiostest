from init import app

from models import User

import routes
import routes_async

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
