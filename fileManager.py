def fullscreenImport():
    fullscreenFile = open(r"data/savings/fullscreen-settings.txt", "r", encoding="utf-8")
    checkStateFullscreen = list(map(lambda x: float(x.rstrip('\n')), fullscreenFile))
    StateFullscreen = int(checkStateFullscreen[0])
    return StateFullscreen


def fullscreenExport(StateFullscreen):
    checkStateFullscreenRewrite = open(r"data/savings/fullscreen-settings.txt", "w")
    checkStateFullscreenRewrite.writelines(str(StateFullscreen))
    checkStateFullscreenRewrite.close()


def languageImport():
    checkWhatLanguage = open(r"data/savings/language-settings.txt", "r")
    whatLanguage = list(map(lambda x: str(x.rstrip('\n')), checkWhatLanguage))
    languageNow = whatLanguage[0]
    checkWhatLanguage.close()
    return languageNow


def languageExport(languageNow):
    checkLanguageRewrite = open(r"data/savings/language-settings.txt", "w")
    checkLanguageRewrite.writelines(str(languageNow))
    checkLanguageRewrite.close()


def heroImport():
    heroFile = open(r"data/savings/hero-settings.txt", "r", encoding="utf-8")
    checkHero = list(map(lambda x: float(x.rstrip('\n')), heroFile))
    hero = int(checkHero[0])
    heroNow = hero
    isGetHero2 = checkHero[1]
    heroFile.close()
    return hero, heroNow, isGetHero2


def heroExport(hero, isGetHero2):
    checkHeroRewrite = open(r"data/savings/hero-settings.txt", "w")
    checkHeroRewrite.writelines([str(hero) + '\n', str(int(isGetHero2))])
    checkHeroRewrite.close()


def volumeImport():
    volumeFile = open(r"data/savings/volume-settings.txt", "r", encoding="utf-8")
    checkActDet = list(map(lambda x: float(x.rstrip('\n')), volumeFile))
    wM = checkActDet[0]
    wS = checkActDet[1]
    volS = wS
    volumeFile.close()
    return wM, wS, volS


def volumeExport(wM, wS):
    checkActDet = open(r"data/savings/volume-settings.txt", "w")
    checkActDet.writelines([str(wM) + '\n', str(wS)])
    checkActDet.close()
