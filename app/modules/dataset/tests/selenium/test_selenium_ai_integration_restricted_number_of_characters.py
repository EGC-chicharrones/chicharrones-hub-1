from selenium import webdriver
from selenium.webdriver.common.by import By


class Test_selenium_ai_integration_restricted_number_of_characters:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testseleniumaiintegrationrestrictednumberofcharacters(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(1)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.find_element(By.LINK_TEXT, "Chatbot").click()
        self.driver.find_element(By.ID, "inputText").click()
        self.driver.find_element(By.ID, "inputText").send_keys(
            "La exploración espacial ha sido uno de los mayores"
            " logros de la humanidad, un esfuerzo constante por comprender el vasto universo que nos rodea y, en última"
            " instancia, nuestra propia existencia. Desde los primeros telescopios de Galileo hasta las misiones de "
            " aterrizaje en Marte, la humanidad ha dado pasos impresionantes en su búsqueda de conocimiento más allá "
            "de nuestro planeta. Sin embargo, a pesar de los avances tecnológicos y científicos que hemos "
            "logrado, el espacio sigue siendo un territorio misterioso, lleno de preguntas sin respuestas y de desafíos"
            "que aún no hemos podido superar.\\n\\nEl inicio de la exploración espacial moderna se remonta a mediados "
            "del siglo XX, con la carrera espacial entre las dos superpotencias de la Guerra Fría: Estados Unidos y la "
            "Unión Soviética. En 1957, la Unión Soviética lanzó el primer satélite artificial, el Sputnik 1, "
            "lo que marcó el comienzo de una nueva era en la que los humanos comenzaban a explorar el espacio exterior."
            "Este evento, aunque inicialmente percibido como una amenaza para la seguridad nacional, también fue un "
            "hito que motivó a Estados Unidos a poner en marcha su propio programa espacial.\\n\\nEn 1961, "
            "el cosmonauta soviético Yuri Gagarin se convirtió en el primer ser humano en viajar al espacio "
            "exterior, un logro que dejó "
            "una huella indeleble en la historia de la exploración espacial. Pero quizás el logro más emblemático de la"
            "exploración espacial fue el alunizaje de la misión Apollo 11, cuando el astronauta Neil Armstrong pisó la "
            "superficie de la Luna en 1969. \"Es un pequeño paso para el hombre, pero un gran salto para la "
            "humanidad\", fueron sus palabras al dar el primer paso sobre la superficie lunar, y ese momento "
            "se convirtió en uno de los más icónicos en la historia del siglo XX.\\n\\nSin embargo, la exploración "
            "de la Luna, aunque un hito importante, solo fue el principio de una serie de misiones más ambiciosas. "
            "A medida que avanzaba la tecnología, los científicos y astronautas comenzaron a poner su mirada más allá "
            "de la órbita terrestre. La estación espacial Mir, lanzada por la Unión Soviética en 1986, y la posterior "
            "Estación Espacial Internacional (EEI) han sido hitos importantes en la construcción de laboratorios "
            "orbitando la Tierra, donde científicos de todo el mundo han podido estudiar los efectos de "
            "la microgravedad y realizar experimentos que no podrían llevarse a cabo en la Tierra."
            "\\n\\nA pesar de estos avances, el espacio sigue siendo un desafío para la humanidad. Los "
            "astronautas que viajan al espacio enfrentan peligros tales como la exposición a radiaciones cósmicas "
            "y la falta de gravedad, lo que afecta a su salud de maneras que aún estamos comenzando a comprender. "
            "La comida y el agua en el espacio son limitadas, y los sistemas de soporte vital son cruciales para "
            "mantener con vida a los astronautas durante sus misiones. A medida que nos aventuramos más lejos, como "
            "la exploración de Marte y más allá, las dificultades logísticas y físicas solo aumentan.\\n\\nUno de los "
            "mayores desafíos de la exploración espacial en las próximas décadas será la creación de tecnología "
            "que permita la colonización de otros planetas. Las misiones a Marte, por ejemplo, enfrentan el obstáculo "
            "de la distancia. Viajar a Marte podría llevar entre seis y nueve meses, lo que implica que los astronautas"
            "estarán expuestos a largos períodos de radiación y aislamiento. Además, la creación de hábitats "
            "autosuficientes en Marte, que proporcionen agua, "
            "aire y alimentos, sigue siendo un problema técnico complejo.\\n\\nLa reciente investigación sobre los "
            "exoplanetas, planetas fuera de nuestro sistema solar, también ha abierto nuevas puertas en la exploración "
            "espacial. Gracias a telescopios como el Hubble y el telescopio espacial James Webb, los astrónomos han "
            "identificado miles de exoplanetas en zonas habitables, lo que ha alimentado la esperanza de que podamos "
            "encontrar vida más allá de la Tierra. Aunque no hemos encontrado evidencia concreta de vida extraterrestre"
            ", el estudio de estos exoplanetas sigue siendo una de las fronteras más emocionantes de la "
            "ciencia.\\n\\nAdemás de la búsqueda de vida en otros planetas, la exploración espacial tiene "
            "muchas aplicaciones prácticas en la Tierra. Los satélites proporcionan información crucial sobre el "
            "clima, la agricultura, el medio ambiente y la comunicación. Las imágenes satelitales nos permiten "
            "fenómenos como huracanes y terremotos, y los avances en la tecnología espacial han tenido un impacto "
            "directo en la mejora de la vida diaria, desde los sistemas de navegación GPS hasta los avances en la."
            "\\n\\nEn los últimos años, la exploración espacial ha dejado de ser exclusiva de las agencias "
            "gubernamentales y ha sido asumida por empresas privadas, como SpaceX, Blue Origin y Virgin Galactic. "
            "Estas empresas están trabajando para hacer que los viajes espaciales sean más accesibles, con el objetivo "
            "final de permitir el turismo espacial y reducir los costos de las misiones.\\n\\nEl futuro de la "
            "exploración espacial es incierto, pero también está lleno de promesas. Si bien los desafíos son enormes, "
            "está más cerca que nunca de comprender los secretos del universo. Tal vez, en las próximas décadas, los  "
            "seres humanos viajarán a otros planetas, descubrirán formas de vida extraterrestre o incluso vivirán la "
            "Tierra. La exploración espacial es, sin lugar a dudas, una de las empresas más emocionantes y "
            "cruciales para el futuro de nuestra especie."
        )
        self.driver.find_element(By.ID, "generateButton").click()
        self.driver.find_element(By.ID, "modalCloseButton").click()
        self.driver.find_element(By.CSS_SELECTOR, "body").click()
