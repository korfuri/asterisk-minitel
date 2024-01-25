import logging
import minitel.tc as tc
import random
from datetime import date
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.database import GetEngine, QuestEntry


@register("fesste", ["index"])
class FessteHome(BaseApp):
    def getLeaderboard(self):
        with Session(GetEngine()) as session:
            stmt = select(QuestEntry.nick, func.count(QuestEntry.quest).label("count")).group_by(QuestEntry.nick).order_by(desc("count")).limit(9)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def interact(self):
        self.m.sendfile(asset("fesste/HOMEPAGE.vdt"))
        scores = self.getLeaderboard()
        for idx, (score, nick) in enumerate(scores):
            self.m.pos(16 + idx, 28)
            self.m._write(tc.tBgColor(tc.clMagenta))
            self.m.print('%02d' % score)
            self.m._write(tc.tBgColor(tc.clBlack))
            self.m.print(' %8s' % nick)
        code = self.m.addInputField(24, 2, 12, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        def goGuide():
            code.contents = 'guide'
            return tc.Break
        self.m.keyHandlers[tc.kGuide] = goGuide
        self.m.handleInputsUntilBreak()
        c = code.contents
        match c:
            case '1':
                c = 'consentement'
            case '2':
                c = 'fstx'
            case '3':
                c = 'annonces'
            case '4':
                c = 'horoscope'
            case '5':
                c = 'guide'
        logging.debug("Code: %s", c)
        self.nextApp = appForCode(c)

@register("consentement", ["consent", "regles", "cons", "regle"])
class ConsentementApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("fesste/consentement.vdt"))
        self.m.handleInputsUntilBreak()

@register("fern")
class FERNApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("fesste/FERN.vdt"))
        self.m.handleInputsUntilBreak()

@register("info", ["infos", "tf1", "afp"])
class InfosApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("TF1banner.vdt"))
        self.m.pos(6, 30)
        d = date.today()
        d.replace(year = 1982)
        self.m.print("%d/%d/%d" %(d.day, d.month, d.year))
        self.m.pos(7, 1)
        slug, title, article = random.choice(self.getNews())
        self.m.textBox(7, 1, 40, 1, slug)
        self.m.textBox(9, 1, 40, 1, title, effects=(tc.ESC + tc.tSetDoubleHeight + tc.tFgColor(tc.clYellow)))
        self.m.textBox(10, 1, 40, 14, article)
        self.m.handleInputsUntilBreak()

    def getNews(self):
        return [
            ('Innovation : double effet kiss cool',
             'GISCORP avale Analtech',
             "Grace a VGE qui alloue plusieurs milliards de francs au departement R&D de la GISCORP, l'OPA a pris fin, Analtech change de nom et devient GISTECH. Cette nouvelle branche de la GISCORP est fin prete et devoilera sa feuille de route a venir au cours du prochain seminaire."
            ),
            ('Politique d\'entreprise',
            'Un seminaire royal pour la GISCORP',
            "Le seminaire organise par la GISCORP aura bien lieu en region parisienne. Notre chef supreme VGE profitera de ces chaleureux locaux mis a notre disposition pour nous y rappeler ses grands projets d'avenir du multivers, positionner le curseur de la valeur travail au sein de la GISCORP, nous presenter le calendrier de son regne.",
             ),
            ('36 15 Top Moumoute',
            'Le Maxitel voit le jour',
            "Dernier projet issu des synergies du groupe et sous la geniale impulsion de notre gouverneur avant-gardiste et touche a tout VGE ; le departement Recherche & Developpement et le service des communications cablees accompagneront la mise en service prochaine de ce nouveau support de communication inter-multivers par ecrans interposes et affichage digital securise. Notre visionnaire supreme en disait encore : c'est une bien belle fenetre ouverte sur l'avenir, esperons que cela n'est pas qu' un simple courant d'air new age.",
             ),
            ('Urbanisme : Chicos ou craignos ?',
            'Le Paris Grandiose ou l\'EPAP',
            "L'EPAP (Elargissement du Petit Anneau Peripherique), ce projet ambitieux d'urbanisation etendu de notre belle capitale, propose par notre merveilleux president a immediatement ete confie a la branche d'exploitation des espaces publiques de la CISCORP : GISMMOBILIER. Un projet prevu pour janvier 1990, ou au plus tard avril mai... enfin non pas mai, y a trop de jours feries, donc plutot pour la rentree. Non pas en septembre ca ne nous arrange pas, avec les gamins, l'ecole tout ca. Disons max pour '94 ou '96. ",
             ),
            ('Transports : c\'est parti mon kiki !',
             'Le Turbo Train: voyager vite et loin',
             "Plus vite, plus loin sans quitter le plancher des vaches, c'etait le defi fou que notre sublime chef d'etat VGE lanca il y a quelques annees aux equipes de la GISCORP. Nom de code THV, transport a haute velocite ; ce petit bijou faconne par la GISNCF, le departement deplacement de la GISCORP sera prochainement ouvert au public. Le prochain grand defi : \"Plus vite, plus loin avec la tete dans les nuages\", de quoi titiller avec joie les cellules reveuses de nos meninges, un moyen de transport transatlantique Brest-Miami.",
             ),
            ('Le futur sera chebran',
             'CD-ROM, Camescope, Rubik\'s Cube...',
             "Non ce n'est pas la liste de courses alimentaires de Luc Marcheciel, heros du roman et succes cinematographique eponyme Les Guerres Du Cosmos par l'ecrivaine,realisatrice et premiere dame de France : Joe Orjluka, mais bien les nouveaux mots et objets qui ont fait leur apparition cette annee.",
             ),
            ('Politique & multivers : lache moi !',
            'Le VGE original claque la porte',
            "Epuise par l'inefficacite des VGE paralleles, notre guide ultime, seule lueur d'espoir dans l'obscurite infini des multivers, a menace lors du grand rassemblement des multiVGE, de prendre le controle de l'ensemble des univers pour y instaurer une voix eclairee prospere, une sorte de rang dans l'oignon de ses pensees universelles alignees sur un seul et meme vecteur.",
             ),
            ('Paris et sa banlieue : le grand boum !',
            'Explosion de la centrale de Creteil',
            "La centrale de Creteil qui marquait le debut du \"plein d'emplois\" en resolvant le probleme du \"non-emploi\", \"feignage\" ou encore \"rienbranlage\", a explose aujourd'hui lors de son inauguration. Les equipes de la GISOS, le service de secours et aide aux victimes de catastrophes d'ampleur a ce qu'on en parle au 20h et qui touchent des populations utiles, s'est rendue sur place pour constater qu'il serait rentable de leur venir en aide.",
             ),
        ]

@register("meteo")
class MeteoApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset('meteo.vdt'))
        self.m.pos(3, 5)
        d = date.today()
        d.replace(year = 1982)
        self.m.print("%d/%d/%d" %(d.day, d.month, d.year))
        self.m.keyHandlers[tc.kSuite] = tc.Break
        self.m.handleInputsUntilBreak()

@register("fstx", ["seminaire", "fesstex", "fesstx", "festx"])
class FstxApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("fesste/fstx.vdt"))
        self.m.handleInputsUntilBreak()

@register("atelier", ["ateliers"])
class AtelierApp(BaseApp):
    def interact(self):
        self.showAtelier()

    def showAtelier(self):
        title = 'MASSAGES AU PIED LEVÉ'
        slug = """Redécouvre tes collègues sous un nouveau jour, exit l’autorité, les missions et les ragots de la machine à café, faites place à la tendresse et à la lenteur pour plonger au fond de soi et de l’autre en douceur.
Interactions physiques sans intention sexuelle / Sensualité (sans génitalité) • implication encadrée • 1H30 • 12 pers. • pratique en solo, en duo et en trio • venez avec des vêtements confortables"""
        self.m.pos(1, 0)
        self.m._write(tc.ESC + tc.tSetDoubleWidth + tc.tFgColor(tc.clRed))
        self.m.print("Atelier")
        self.m._write(tc.ESC + tc.tSetNormalHeight + tc.tFgColor(tc.clYellow))
        self.m.print("%26s" % "Vendredi 18:00")

        self.m.pos(2, 0)
        pad = (40 - len(title)) // 2 - 1
        self.m.print(" " * pad)
        self.m._write(tc.ESC + tc.tStartUnderline + b' ')
        self.m.print(title)
        self.m._write(tc.ESC + tc.tEndUnderline)

        self.m.pos(3, 1)
        self.m.print(slug.replace('\n', '\r\n'))
        self.m.handleInputsUntilBreak()


@register("legends", ["legendes"])
class LegendsApp(BaseApp):
    """A tribute to winners of previous quest games."""
    def interact(self):
        self.m.sendfile(asset("legends.vdt"))
        self.m.handleInputsUntilBreak()
