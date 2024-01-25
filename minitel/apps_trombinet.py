from minitel.apps import BaseApp, register
from minitel.assets import asset
from minitel.ImageMinitel import ImageMinitel
import minitel.tc as tc
from PIL import Image
import logging
import os
import pathlib
import random


@register("trombinet", ["facebook", "linkedin", "google+"])
class FacebookApp(BaseApp):
    def interact(self):
        self.m.reset()
        self.m.sendfile(asset("trombinet.vdt"))

        is_image = random.choice([True, False, False, False])
        if is_image:
            imgs = os.listdir(asset("trombinet/pics"))
            i = random.choice(imgs)
            image = Image.open(asset("trombinet/pics/" + i))
            image.thumbnail((80, 60), Image.LANCZOS)
            image_minitel = ImageMinitel()
            image_minitel.importer(image)
            self.m.pos(1, 1)
            self.m.setTextMode()
            tags = pathlib.Path(i).stem.split('_')
            self.m.print((' '.join([' #%s' % t for t in tags])).strip(' '))
            image_minitel.envoyer(self.m, 1, 2)
        else:
            status = self.get_status()
            self.m.textBox(2, 1, 40, 20, status)

        self.m.pos(23, 1)
        self.m.setTextMode()
        self.m.print(self.get_poster())
        def repeat():
            self.nextApp = 'A'
            return tc.Break
        self.m.keyHandlers[tc.kSuite] = repeat
        self.m.pos(23, 32)
        self.m.print(self.get_likes())  # TODO
        self.m.handleInputsUntilBreak()

    def get_poster(self):
        first = random.choice([
            'Nicolas',
            'Julien',
            'Aurélie',
            'Sébastien',
            'Céline',
            'Emilie',
            'David',
            'Laëtitia',
            'Cédric',
            'Guillaume',
            'Elodie',
            'Stéphanie',
            'Virginie',
            'Audrey',
            'Jérôme',
            'Marie',
            'Alexandre',
            'Julie',
            'Christophe',
            'Vincent',
            'Sabrina',
            'Frédéric',
            'Sophie',
            'Thomas',
            'Vanessa',
            'Mathieu',
            'Grégory',
            'Caroline',
            'Olivier',
            'Romain',
            'Mickael',
            'Ludovic',
            'Stéphane',
            'Jessica',
            'Anthony',
            'Delphine',
            'Mélanie',
            'Angélique',
            'Sandrine',
            'Sylvain',
            'Damien',
            'Arnaud',
            'Laurent',
            'Nathalie',
            'Pierre',
            'Fabien',
            'Jonathan',
            'Benoit',
            'Benjamin',
            'Jérémy',
        ])
        return '@%s' % first

    def get_likes(self):
        return '%02d' % random.randrange(0, 99)

    def get_status(self):
        statuses = [
            "Hello le Maxitel !",
            "Premier post sur TrombiNet, j'ai hâte de retrouver plein d'amis ici !",
            "Hier soir, j'ai assisté au match de l'équipe nationale et je dois dire que j'étais époustouflé ! Les joueurs ont donné leur maximum et ont réussi à marquer un but incroyable dans les dernières minutes du match. L'ambiance dans le stade était électrique et je n'ai jamais ressenti une telle ferveur pour notre équipe. Bravo à eux pour cette victoire et merci pour cette soirée mémorable ! #AllezLesBleus #FiertéNationale #1999",
            "Hier soir, j'ai assisté au match de l'équipe nationale et je n'ai qu'une chose à dire : quelle ambiance incroyable ! Les supporters étaient en folie et les joueurs ont tout donné sur le terrain. Même si nous avons perdu, je suis fier de notre équipe et de son parcours jusqu'à présent. En route pour la victoire ! Allez les Bleus #MatchDeFoot #EquipeNationale #FierDeMonPays #1999",
            "Quel match incroyable hier soir pour notre équipe nationale de foot ! Les joueurs ont tout donné sur le terrain et nous ont offert une victoire mémorable. La joie et la fierté se lisent sur tous les visages ce matin, et je ne peux m'empêcher de revivre chaque but avec émotion. Merci à tous pour ce moment inoubliable, vive le football et vive notre équipe ! #AllezLesBleus #1999 #VictoireHistorique",
            "Quelle soirée incroyable hier, quel match de foot époustouflant de notre équipe nationale! Nos joueurs ont tout donné sur le terrain et ont su nous faire vibrer jusqu'à la dernière minute. On peut être fiers de notre équipe et de leur performance. Et cette ambiance dans les tribunes, c'était magique! Merci à tous les supporters d'avoir été présents pour encourager notre équipe. #AllezLesBleus #FiersDeNotreEquipe #1999",
            "Quel match incroyable hier soir ! L'équipe nationale a donné tout son cœur sur le terrain et a remporté une victoire éclatante ! Les supporters étaient en délire, les chants résonnaient dans le stade. C'était une soirée mémorable, une fierté pour notre pays. On peut dire que nos joueurs ont écrit l'histoire du football ce soir. Bravo à eux et vive l'équipe nationale ! #1999 #matchdefoot #victoire #fiersdenotreéquipe",
            "Hier soir, quelle soirée incroyable ! Notre équipe nationale a remporté le match de foot contre nos rivaux historiques. Les rues étaient remplies de drapeaux et de chants de supporters enthousiastes. Les joueurs ont tout donné sur le terrain et ont prouvé leur talent. C'est une fierté de voir notre pays uni derrière cette passion commune. Bravo à nos champions ! Vive le football et vive notre équipe nationale ! #1999 #matchdefoot #fierté #equipefrance"
            "Quel match incroyable hier soir ! L'équipe nationale a donné le meilleur d'elle-même et a remporté la victoire haut la main ! J'ai encore du mal à réaliser que nous avons battu nos rivaux historiques. Les joueurs ont été fantastiques et l'ambiance dans le stade était électrisante. Je suis tellement fier de notre équipe nationale, c'est sûr que nous allons faire une belle performance lors de la prochaine Coupe du Monde ! #AllezLesBleus #1999 #FiertéNationale",
            "Hier soir, j'ai vibré devant le match de l'équipe nationale, quelle intensité ! On a crié, on a pleuré, on a chanté, on a vécu chaque but avec passion. Malgré la défaite, nos joueurs ont montré un esprit d'équipe admirable. Bravo à eux ! Et merci pour cette soirée inoubliable. Allez, on se remet de nos émotions en écoutant du Britney Spears et en jouant à la Game Boy. #SupportersFidèles #AllezLesBleus #1999 #Footballmania",
            "Hier soir, j'ai eu la chance d'assister au match de l'équipe nationale au stade. Quelle ambiance incroyable ! Les supporters étaient en feu et nos joueurs ont donné le meilleur d'eux-mêmes sur le terrain. Malheureusement, la victoire nous a échappé mais nos joueurs ont montré leur détermination et leur talent. Fier de notre équipe et de notre pays ! Allez les Bleus ! #MatchDeFoot #EquipeNationale #FiersDeLaFrance",
            "Quelle soirée mémorable hier soir ! Notre équipe nationale a donné tout son cœur sur le terrain et a remporté une victoire éclatante face à nos rivaux ! Quelle fierté de voir nos joueurs donner le meilleur d'eux-mêmes pour notre pays. On a vibré, on a chanté, on a célébré ensemble cette belle performance. Merci à tous les supporters présents au stade, vous avez été incroyables. Allez les bleus ! #FiersDeNotreEquipe #ViveLeFootball #1999",
        ]
        return random.choice(statuses)
