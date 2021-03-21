import math
import re

from typing import Optional

from bs4 import BeautifulSoup, NavigableString

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.utils.Utils import Utils
from config import shared
from selenium.webdriver import Chrome

class TitleFinder:

    # todo: we could add here list of cities
    title_blacklist = ["Odběr novinek", "Nejbližší uvedení", "Říjen", "všechnapředstavení", "Menu", "Hledání",
                       "Podrobné nastavení", "Back Button Back", "Vaše soukromí", "Více informací", "Koncerty",
                       "Připravované koncerty", "kapela", "Back to the top", "doprovodný program",
                       "Praha", "Vstupenky", "Koupit", "Termíny", "Kontakty", "Mapa", "Doprava",
                       "Termíny", "Profil", "Tento měsíc", "Základní informace", "Štítky", "RSS", "příspěvky",
                       "Nejnovější příspěvky", "Rubriky", "Děkujeme za podporu", "Aktuality", "Naše akce",
                       "Registrační podmínky", "PDF", "DOC", "XLSX", "XLS", "Přílohy", "Zjistit více",
                       "Nejbližší akce", "Kalendář akcí", "Fotogalerie akcí", "Provozovatel", "Časová náročnost",
                       "Akce v okolí", "celý text", "Svátek", "Návštěvnost", "Aktuální počasí", "Senioři",
                       "Univerzální překladač", "Hlášení", "Mobilní aplikace", "Obsah", "Navigace",
                       "Adresa", "Úřední hodiny", "Vyhledávání", "Facebook", "Ohodnoťte tento produkt",
                       "Vstupné", "Více informací a kontakt", "Kdy se akce koná", "Dejte o akci vědět přátelům!",
                       "Témata webu", "Navigace menu", "Místo konání", "Podrobnosti", "Redakce", "Přidat do kalendáře",
                       "Další termíny akce", "V okolí doporučujeme...", "Aktuální koncerty", "Další akce v tomto místě",
                       "Umělci", "Information about the concert", "Tickets", "Předprodej online", "Novinky emailem",
                       "Web", "E-shop", "Detail akce", "Informace o akci", "Naše tipy...",
                       "Další informace", "Doporučujeme", "Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota",
                       "Neděle", "Předchozí", "Tradiční akce", "Akce", "Otevírací doba", "Místo", "Číst více...",
                       "zobrazit celý text", "Další akce pro veřejnost", "Zobrazit archiv aktualit",
                       "Čas", "Popis", "Naše tipy", "Odloženo", "Zrušeno", "Připravujeme", "Kontaktujte nás",
                       "Fotogaléria", "Aktualita", "Adresa a kontakt", "Parkování", "Vrácení vstupenek", "a",
                       "Novinky", "Popis", "Podobné akce", "vstupenky", "Navigovat", "Program", "Podobné události",
                       "Headlines", "Kontakt", "Adresát", "Archiv aktualit", "Mohlo by vás zajímat", "Sdílet obsah",
                       "Klasická verze", "Podmínky", "Leden", "LEDEN", "Zakázka", "Přijímáme online platby",
                       "Související články", "Mohlo by vás zajímat", "Zprávy", "Autor", "Hlavní zprávy", "Sdílet obsah",
                       "Info", "News", "Zrušeno", "ZRUŠENO", "zrušeno", "Zobrazit více →", "Navštivte také", "Podmínky výzvy",
                       "Poslední hodnocení", "Úvodní stránka", "Najdete nás", "zde", "AKTUALITY", "home", "Výběr článků",
                       "KVĚTEN", "Platnost voucheru", "Odehrané koncerty", ".", "•"
                       ]

    @staticmethod
    def find(soup, is_single_event=False, near_containers = []) -> Optional[Title]:
        if is_single_event:
            return TitleFinder._find_internal_single_event(soup, near_containers)

        # sometimes list events do not have proper title
        # so if the event container is content of main title, it is likely name of the event
        # todo: this operation is quite resource heavy, might be good idea to cache it for each site
        main_title = TitleFinder._find_internal_single_event(soup, near_containers)
        use_main_title = False
        if main_title is not None:
            main_title_regex_compiled = re.compile(re.escape(main_title.value), flags=re.IGNORECASE)
            if soup.find(text=main_title_regex_compiled) is not None:
                use_main_title = True

        title_from_list = TitleFinder._find_internal(soup, True, True)
        if use_main_title and title_from_list is not None:
            title_from_list.alternative_value = main_title.value

        if title_from_list is not None and title_from_list.alternative_value is None:
            container = soup
            parent = soup.parent
            while parent is not None:
                container = parent
                parent = parent.parent

            title_element = container.find("title")
            if title_element is not None:
                title_from_list.alternative_value = Utils.clean(title_element.getText())

        return title_from_list

    @staticmethod
    def _find_internal(soup, recursive, try_headless=False):
        driver = shared.driver
        if try_headless is True and driver is not None:
            # assert "Python" in driver.title
            css_path = Utils.getCSSPath(soup)
            print(css_path)
            elems = driver.find_elements_by_css_selector(css_path + " *")
            biggest_font_size = 0
            biggest_font_size_element = None
            for elem in elems:
                font_size = int(float(elem.value_of_css_property("fontSize").strip("px")))
                cleaned_text = Utils.clean(elem.text)
                if font_size > biggest_font_size and cleaned_text != "" and cleaned_text not in TitleFinder.title_blacklist:
                    biggest_font_size = font_size
                    biggest_font_size_element = elem

            if biggest_font_size_element is not None and biggest_font_size > 15:
                text = Utils.clean(biggest_font_size_element.text)
                return Title(text, "", None)

        title = soup.find(["h1"], recursive=recursive)
        if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
            title = soup.find("h2", recursive=recursive)
            if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                title = soup.find("h3", recursive=recursive)
                if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                    title = soup.find("h4", recursive=recursive)
                    if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                        title = soup.find("h5", recursive=recursive)
                        if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                            # for list event, it is possible to contain link to event and usually there is either
                            # event name (we want that) or just url (we do not want that)
                            links = soup.find_all("a", recursive=recursive)
                            if len(links) > 0:
                                link = links[0]

                                if link is not None and "www" not in link.getText() and ".cz" not in link.getText() and "http" not in link.getText() and Utils.clean(link.getText()) != "" and TitleFinder.__title_contains_only_date(link) is False:
                                    title = link

                                if title is None and len(links) > 1:
                                    link = links[1]
                                    if link is not None and "www" not in link.getText() and ".cz" not in link.getText() and "http" not in link.getText() and Utils.clean(link.getText()) != "" and TitleFinder.__title_contains_only_date(link) is False:
                                        title = link

        if recursive is True and (title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(
                title.getText()) == "" or TitleFinder.__title_contains_only_date(title)):
            title = soup.find("strong", recursive=recursive)

        # Traverse up (when traversing up, we want to try find title only in direct children, not in all structure.
        # That could accidentally get title from other event.
        if (title is None or Utils.clean(Utils.get_first_line(title.getText())) in TitleFinder.title_blacklist) and soup.parent is not None:
            return TitleFinder._find_internal(soup.parent, False)

        is_from_title_element = False
        if title is None or Utils.clean(title.getText()) in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "":
            title = soup.find("title")
            is_from_title_element = True

        if title is None or Utils.clean(title.getText()) in TitleFinder.title_blacklist:
            return None

        text = Utils.get_first_line(title.getText())
        text = Utils.clean(text)
        aleternative_text = ""
        if len(text) < 50:
            container = soup
            parent = soup.parent
            while parent is not None:
                container = parent
                parent = parent.parent
            h1 = container.find(["h1"], recursive=recursive)
            if h1 is not None and Utils.clean(h1.getText()) not in TitleFinder.title_blacklist and Utils.clean(h1.getText()) != "":
                aleternative_text = Utils.clean(h1.getText()) + " - " + text

        return Title(text, aleternative_text, title, is_from_title_element)

    @staticmethod
    def __title_contains_only_date(title):
        text = title.getText()
        if len(text) < 5:
            return False
        dates = DateFinder.find(title, False)
        for date in dates:
            text = text.replace(date.realValue, "")

        text = Utils.clean(text)
        if len(text) < 5:
            return True

        return False


    @staticmethod
    def _find_internal_single_event(soup, near_containers = []):
        sibling = soup.find_next_sibling()
        if sibling is not None:
            soup_next_sibling_sourceline = sibling.sourceline
        else:
            soup_next_sibling_sourceline = 999999
        container = soup
        parent = soup.parent
        while parent is not None:
            container = parent
            parent = parent.parent

        titles = container.find_all(["h1", "h2", "h3", "h4", "h5"])

        lowest_score = 9999
        title = None
        for t in titles:
            # we are only interested in headings before the container, that is achieved by calculating the
            # sourceline of next sibling to the soup
            if t.sourceline > soup_next_sibling_sourceline:
                continue

            if Utils.clean(t.getText()) in TitleFinder.title_blacklist or Utils.clean(t.getText()) == "":
                continue

            # score = Utils.get_depth(t)
            score = 0
            if t.name == "h1":
                score += 1
            if t.name == "h2":
                score += 5
            if t.name == "h3":
                score += 10
            if t.name == "h4":
                score += 15
            if t.name == "h5":
                score += 20

            for near_container in near_containers:
                if isinstance(near_container, NavigableString):
                    near_sourceline = near_container.parent.sourceline
                else:
                    near_sourceline = near_container.sourceline
                # this checks for distance in html (max penalty 30)
                # log used here - if something is further from container, linear penalization would be too much
                # and just lowering the maximum would not reflect that something is further
                # (the + 0.1 prevents getting log from 0 which is undefined operation)
                score += min([10, math.log(abs(near_sourceline - t.sourceline) + 0.1) * 3])
                # this issues depth penalty (less difference in depth means less penalty, max 10)
                score += 10 - min(
                    [10, Utils.get_depth(Utils.lowest_common_ancestor(near_container, t))]
                )
            if score < lowest_score and t.getText() is not "":
                lowest_score = score
                title = t

        is_from_title_element = False
        if title is None:
            title = soup.find("title")
            is_from_title_element = True
        if title is None:
            return None

        title_element = soup.find("title")
        alternative_title = ""
        if title_element is not None:
            alternative_title = Utils.clean(title_element.getText())

        text = Utils.get_first_line(title.getText())
        text = Utils.clean(text)

        return Title(text, alternative_title, title, is_from_title_element)
