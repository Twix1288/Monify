from MonifyFlask import app
import ssl
if __name__ == "__main__":
    context = ('local.crt', 'local.key')  # certificate and key files
    app.run(debug=True)
