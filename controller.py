from views import *

if __name__=='__main__':
    test_db.create_all()
    test_db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5151)
