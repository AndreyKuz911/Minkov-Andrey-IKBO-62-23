import unittest
from script import ConfigTranslator  # Импортируем ConfigTranslator из script.py

class TestConfigTranslator(unittest.TestCase):
    def test_translate_server_config(self):
        toml_data = {
            "server": {
                "host": "localhost",
                "port": 8080,
                "ssl": True
            }
        }
        translator = ConfigTranslator(toml_data)
        output = translator.translate()
        expected_output = '''server = {
    host : "localhost";
    port : 8080;
    ssl : "True";
}'''
        self.assertEqual(output.strip(), expected_output.strip())

    def test_translate_database_config(self):
        toml_data = {
            "database": {
                "type": "PostgreSQL",
                "max_connections": 20,
                "credentials": {
                    "user": "admin",
                    "password": "secret"
                }
            }
        }
        translator = ConfigTranslator(toml_data)
        output = translator.translate()
        expected_output = '''database = {
    type : "PostgreSQL";
    max_connections : 20;
    credentials : {
    user : "admin";
    password : "secret";
};
}'''
        self.assertEqual(output.strip(), expected_output.strip())

    def test_translate_user_settings(self):
        toml_data = {
            "user_settings": {
                "theme": "dark",
                "notifications": {
                    "email": False,
                    "sms": True
                },
                "favorites": ["Python", "OpenAI", "AI"]
            }
        }
        translator = ConfigTranslator(toml_data)
        output = translator.translate()
        expected_output = '''user_settings = {
    theme : "dark";
    notifications : {
    email : "False";
    sms : "True";
};
    favorites : << "Python", "OpenAI", "AI" >>;
}'''
        self.assertEqual(output.strip(), expected_output.strip())

if __name__ == "__main__":
    unittest.main()
