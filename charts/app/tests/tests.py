from django.test import TestCase, Client


class ChartTestCases(TestCase):
    def test_con_x_y(self):
        c = Client()
        r = c.get("/?x=[1,2,3,4,5]&ys=[[5,4,3,3,3]]&labels=[%271%20eje%20ys%27]&divId=chart")
        print r.status_code
        self.assertEqual(r.status_code, 200)

    def test_con_x_ys(self):
        c = Client()
        r = c.get("/?x=[1,2,3,4,5]&ys=[[5,4,3,3,3]]&labels=[%271%20eje%20ys%27]&divId=chart")
        self.assertEqual(r.status_code, 200)

    def test_con_x_2ys(self):
        c = Client()
        r = c.get("?x=[1,2,3,4,5]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27dos%20ejes%20ys%27,%20%27mi%20otra%20label%27]&divId=chart")
        self.assertEqual(r.status_code, 200)

    def test_con_x_2ys_Stacked(self):
        c = Client()
        r = c.get("/?x=[1,2,3,4,5]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27dos%20ejes%20ys%20stacked%27,%20%27mi%20otra%20label%27]&divId=chart&stacked=true")
        self.assertEqual(r.status_code, 200)

    def test_con_fechas_x(self):
        c = Client()
        r = c.get("/?x=[%272017-06-15%27,%272017-06-16%27,%272017-06-17%27,%272017-06-18%27,%272017-06-19%27]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27eje%20x%20con%20fecha%27,%20%27mi%20otra%20label%27]&divId=chart&xType=%27date%27&stacked=%27true%27&colors=[#FAA519,%27blue%27]")
        self.assertEqual(r.status_code, 200)

    def test_con_y_ys(self):
        c = Client()
        r = c.get("/?x=[%272017-06-15%27,%272017-06-16%27,%272017-06-17%27,%272017-06-18%27,%272017-06-19%27]&y=[3,3,3,3,3]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27Mi%20label%27,%27con%20una%20y%20y%20una%20ys.%20debe%20ignorar%20la%20y%27,%27el%20tercero%27]&divId=chart&xType=%27date%27&stacked=%27true%27&colors=[#FAA519,%27blue%27]")
        self.assertEqual(r.status_code, 200)

    def test_area_char_con_fecha(self):
        c = Client()
        r = c.get("/?x=[%272017-06-15%27,%272017-06-16%27,%272017-06-17%27,%272017-06-18%27,%272017-06-19%27]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27prueba%20area%20chart%20con%20fecha%27,%27label%27]&divId=chart&xType=%27date%27&kind=AreaChart")
        self.assertEqual(r.status_code, 200)

    def test_area_char_con_fecha_stacked(self):
        c = Client()
        r = c.get("/?x=[%272017-06-15%27,%272017-06-16%27,%272017-06-17%27,%272017-06-18%27,%272017-06-19%27]&ys=[[5,4,3,3,3],[1,2,3,4,5]]&labels=[%27prueba%20area%20chart%20con%20fecha%20STACKED%27,%27label%27]&divId=chart&xType=%27date%27&kind=AreaChart&stacked=true")
        self.assertEqual(r.status_code, 200)

    def test_hist_simple(self):
        c = Client()
        r = c.get("/hist/?x=[1,2,3,4,5,1,1,1]&labels=[%27prueba%20siple%20de%20hist%27]&divId=chart")
        self.assertEqual(r.status_code, 200)

    def test_hist_sin_divid(self):
        c = Client()
        r = c.get("/hist/?x=[1,2,3,4,5,1,1,1]&labels=[%27hist%20sin%20divId%27]")
        self.assertEqual(r.status_code, 200)

    def test_pie_chart(self):
        c = Client()
        r = c.get("/?x=[15,10]&xType=string&labels=[%27A%20-%20label%27,%27B%20-%20label%27]&kind=PieChart")
        self.assertEqual(r.status_code, 200)


