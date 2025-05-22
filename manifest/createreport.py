from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import date


class CreateReport:
    def __init__(self, date):
        self.width, self.height = A4
        self.line_height = self.height - 1.5 * cm
        self.c = None
        self.date = date
        # [[value for lodge state postcode direct], [lodge state area, other state area],
        # [lodge state residue, other state residue]]
        self.overall_totals = [[0, 0], [0, 0], [0, 0]]
        self.current_totals = [0, 0, 0]  # Postcode direct, area direct, residue

    def create_pdf(self, path, categories, pub_title, print_post_number, weight, standard, total_articles, article_size
                   , pricing):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.create_header(pub_title, print_post_number, weight, standard, total_articles, article_size,
                           "Print Post Manifest")
        self.draw_table(categories)
        self.c.showPage()
        self.line_height = self.height - 1.5 * cm
        self.create_header(pub_title, print_post_number, weight, standard, total_articles, article_size,
                           "Print Post Pricing Summary")
        self.draw_prices(categories, pricing, weight, standard, article_size)
        self.c.save()

    def draw_prices(self, categories, pricing, weight, standard, article_size):
        # Start with a large gap
        self.line_height -= 25

        weight_range = pricing.determine_weight_range(weight)

        self.c.drawString(2 * cm, self.line_height, "Weight range: " + weight_range + "g")
        self.line_height -= 25

        if article_size == "Small":
            self.draw_small_prices(categories, pricing, standard)
        else:
            self.draw_large_prices(categories, pricing, weight_range, standard)

    def draw_price_columns(self):
        columns = [2 * cm, 2 * cm + 200, 2 * cm + 350, self.width-2*cm]
        text = ["", "Unit $", "Volume", "Total $"]
        for i in range(1, len(columns)):
            self.c.drawRightString(columns[i], self.line_height, text[i])
        return columns

    def draw_small_prices(self, categories, pricing, standard):
        if standard == "Priority":
            unit_costs = pricing.priority_pricing
        else:
            unit_costs = pricing.regular_pricing

        columns = self.draw_price_columns()
        sub_tables = ["Same State", "Other State"]
        # Volumes extacts the same state and other state volumes for residue from totals as small can only be residue
        volumes = [self.overall_totals[2][0], self.overall_totals[2][1]]
        total_cost = []
        for i in range(0, len(sub_tables)):
            self.c.setFont("Helvetica-Bold", 11)
            self.line_height -= 15
            self.c.drawString(columns[0], self.line_height, sub_tables[i])
            self.c.setFont("Helvetica", 11)
            self.line_height -= 15
            self.c.drawString(columns[0], self.line_height, "   Residue")
            self.c.drawRightString(columns[1], self.line_height, unit_costs[i])
            # Volume, total here
            self.c.drawRightString(columns[2], self.line_height, str(volumes[i]))
            total_cost.append(volumes[i]*float(unit_costs[i]))
            self.c.drawRightString(columns[3], self.line_height, "{:.2f}".format(total_cost[i]))
            self.draw_line()

        self.line_height -= 10
        self.draw_final_cost(sum(total_cost))

    def draw_large_prices(self, categories, pricing, weight_range, standard):

        columns = self.draw_price_columns()
        # Getting costs for same state, other state for postcode direct, area direct, and residue
        if standard == "Priority":
            costs = pricing.priority_pricing
        else:
            costs = pricing.regular_pricing

        sub_tables = ["Same State", "Other State"]
        total_cost = []
        self.line_height -= 15

        for i in range(0, len(sub_tables)):
            self.c.setFont("Helvetica-Bold", 11)
            self.c.drawString(columns[0], self.line_height, sub_tables[i])
            self.c.setFont("Helvetica", 11)
            self.line_height -= 15

            # If same state we have postcode direct to consider
            if i == 0:
                categories = ["   Postcode Direct", "   Area Direct", "   Residue"]
                unit_costs = [costs[0][weight_range], costs[1][weight_range][i], costs[2][weight_range][i]]
                volumes = [self.overall_totals[0][i], self.overall_totals[1][i], self.overall_totals[2][i]]
            else:
                categories = ["   Area Direct", "   Residue"]
                unit_costs = [costs[1][weight_range][i], costs[2][weight_range][i]]
                volumes = [self.overall_totals[1][i], self.overall_totals[2][i]]

            for j in range(0, len(categories)):
                # Print category name we are at
                self.c.drawString(columns[0], self.line_height, categories[j])

                # Print unit cost for category
                self.c.drawRightString(columns[1], self.line_height, unit_costs[j])

                # Print volume we are at
                self.c.drawRightString(columns[2], self.line_height, str(volumes[j]))

                # Print total cost for that category
                total_cost.append(float(volumes[j])*float(unit_costs[j]))
                self.c.drawRightString(columns[3], self.line_height, "{:.2f}".format(total_cost[-1]))

                self.line_height -= 15
            self.line_height += 5
            self.draw_line()
        self.draw_final_cost(sum(total_cost))

    def draw_final_cost(self, cost):
        #self.draw_line()
        self.c.setFont("Helvetica-Bold", 13)
        self.c.drawString(2*cm, self.line_height, "Total: $" + "{:.2f}".format(cost))

    def draw_table(self, categories):
        columns = self.draw_table_header()
        self.draw_table_contents(categories, columns)

    def draw_table_contents(self, categories, columns):
        font_bold, font, size = "Helvetica-Bold", "Helvetica", 11
        format_total = lambda x: "-" if x == 0 else str(x)

        for state in categories.keys():
            self.c.setFont(font, size)
            articles = categories[state]

            if len(articles) > 0:
                # If there are any postcode directs they are always first on the list
                # See sort for the format of these articles. Postcode direct differs in format to area direct and residue
                i = 0
                while i < len(articles):
                    if articles[i][0] == "Postcode":
                        i = self.draw_postcode_direct(i, articles, state, columns)
                    elif articles[i][0] == "Area":
                        # Header for column
                        self.c.drawString(2 * cm, self.line_height, state + " " + articles[i][1])
                        self.draw_area_direct(articles[i], columns)

                        # If article direct is the last entry then get rid of the extra space added by the method
                        i += 1
                        if i == len(articles):
                            self.line_height += (size + 5)

                    elif articles[i][0] == "Residue":
                        self.draw_residue(articles[i], columns, state)
                        i += 1
                    else:
                        print("error", state, articles)
                        raise IndexError()
                # We have finished a state so we should draw a line and write the totals.
                self.draw_line()
                # TODO: Extra blank line of space since if 1 Area Direct it still adds blank line
                text = ["Total: " + state, "", format_total(self.current_totals[0]), format_total(self.current_totals[1]),
                        format_total(self.current_totals[2])]

                self.c.setFont(font_bold, size)
                self.c.drawString(2 * cm, self.line_height, "Total: " + state)
                for j in range(1, len(text)):
                    self.c.drawRightString(columns[j], self.line_height, text[j])

                self.draw_line()

                # At the end of the state add the current_totals to the overall totals
                self.add_current_totals(state)

        self.draw_line()
        text = ["TOTAL SUMMARY", "", format_total(sum(self.overall_totals[0])),
                format_total(sum(self.overall_totals[1])), format_total(sum(self.overall_totals[2]))]

        self.c.drawString(2 * cm, self.line_height, text[0])
        for j in range(1, len(text)):
            self.c.drawRightString(columns[j], self.line_height, text[j])
        self.draw_line()

    def add_current_totals(self, state):
        lodgement = "VIC"
        # Get to add to the lodgement state total or other state total
        idx = 0 if state == lodgement else 1
        for i in range(0, len(self.current_totals)):
            self.overall_totals[i][idx] += self.current_totals[i]
        self.current_totals = [0, 0, 0]

    def check_line_height(self, font="Helvetica", size=11):
        # If we are about to draw of the page then set up a new page.
        if self.line_height < 1.5 * cm:
            self.c.showPage()
            self.c.setFont(font, size)
            self.line_height = self.height - 1.5 * cm
            return True
        return False

    def draw_postcode_direct(self, i, articles, state, columns, size=11):
        indicator = articles[i][1]
        self.c.drawString(2 * cm, self.line_height, state + " " + indicator)
        # For all the postcode directs at that presort indicator
        for j in range(0, len(articles[i][2])):
            self.current_totals[0] += articles[i][2][j][1]
            text = ["", articles[i][2][j][0], str(articles[i][2][j][1]), "-", "-"]
            for k in range(1, len(text)):
                self.c.drawRightString(columns[k], self.line_height, text[k])  # Adding postcode
            self.line_height -= (size + 5)
            self.check_line_height()

        # Undoing last iteration when nothing is after it.
        self.line_height += (size + 5)
        self.check_line_height()

        # Check if the next index is an area direct under the same sort division
        i += 1
        if i < len(articles) and articles[i][0] == "Area" and articles[i][1] == indicator:
            self.draw_area_direct(articles[i], columns)
            i += 1

        return i

    def draw_area_direct(self, article, columns, size=11):

        text = ["", "-", "-", str(article[2]), "-"]
        self.current_totals[1] += article[2]
        for k in range(1, len(text)):
            self.c.drawRightString(columns[k], self.line_height, text[k])  # Adding postcode

        self.line_height -= (size + 5)
        self.check_line_height()

    def draw_residue(self, article, columns, state):
        self.c.drawString(2 * cm, self.line_height, state + " Residue")

        self.current_totals[2] += article[2]
        text = ["", "-", "-", "-", str(article[2])]
        for k in range(1, len(text)):
            self.c.drawRightString(columns[k], self.line_height, text[k])  # Adding postcode

        self.check_line_height()

    def draw_table_header(self):
        font, size = "Helvetica-Bold", 11
        self.c.setFont(font, size)
        text = ["Division", "Postcode", "Postcode Direct", "Area Direct", "Residue"]
        columns = [2 * cm + self.c.stringWidth(text[0], font, size), 2 * cm + 146, 2 * cm + 283, 2 * cm + 385,
                   self.width - 2 * cm]
        self.c.drawString(2 * cm, self.line_height, "Sort")

        self.line_height -= (size + 5)

        for i in range(0, len(columns)):
            self.c.drawRightString(columns[i], self.line_height, text[i])

        self.draw_line(size)
        return columns

    def create_header(self, pub_title, post_number, weight, standard, total_articles, article_size, header_name):
        # TODO: Low priority make state more modular
        lodgement = "VIC"
        fonts = ["Helvetica", "Helvetica-Bold"]

        # Creating first row of manifest
        self.draw_header_row(["", header_name], ["Article size: ", article_size], fonts)

        # Creating second row containing company and date of lodgement
        curr_date = self.date.strftime("%d/%m/%Y")
        self.draw_header_row(["Company: ", "Maroondah Printing"], ["Date of lodgement: ", curr_date], fonts)

        # Creating third row containing publication title and print post number
        self.draw_header_row(["Publication Title: ", pub_title], ["Print Post Number: ", post_number], fonts)

        # Creating fourth row containing total articles and weight per article
        self.draw_header_row(["Total Articles: ", str(total_articles)], ["Weight per Article: ", str(weight) + "g"],
                             fonts)

        # Creating fifth and final row of the header
        self.draw_header_row(["Statement of Lodgement: ", lodgement], ["Delivery Standard: ", standard], fonts)

    def draw_header_row(self, column1, column2, fonts, size=13):
        """
        TODO: Check for line wrappings
        Writes to the canvas a singular row for the header including a line break for the next line
        :param column1: A tuple of: (column name: str, value: str). The value will be placed in bold.
        :param column2: A tuple of: (column name: str, value: str). The value will be placed in bold.
        :param fonts: A tuple of: (non-bold-font, bold font)
        :param size: The size of the text. Rest of the program uses a default, but headers have a different size
        """

        # Calculating second row width
        width_2 = round(self.width * 2 / 3) - 2 * cm

        # Drawing all text for values
        self.c.setFont(fonts[0], size)

        self.c.drawString(2 * cm, self.line_height, column1[0])
        self.c.drawString(width_2, self.line_height, column2[0])

        self.c.setFont(fonts[1], size)
        length = self.c.stringWidth(column1[0], fonts[0], size)
        self.c.drawString(2 * cm + length, self.line_height, column1[1])

        length = self.c.stringWidth(column2[0], fonts[0], size)
        self.c.drawString(width_2 + length, self.line_height, column2[1])

        # Drawing line underneath row
        self.draw_line(size)

    def draw_line(self, size=11):
        # Drawing line underneath row
        self.line_height -= 10
        if not self.check_line_height():
            self.line_height += 5

        self.c.line(2 * cm, self.line_height, self.width - 2 * cm, self.line_height)
        self.line_height -= (size + 5)
