def fullscreenImport():
    fullscreenFile = open(r"../data/fullscreen-settings.txt", "r", encoding="utf-8")
    checkStateFullscreen = list(map(lambda x: float(x.rstrip('\n')), fullscreenFile))
    StateFullscreen = int(checkStateFullscreen[0])
    fullscreenFile.close()
    return StateFullscreen


def fullscreenExport(StateFullscreen):
    checkStateFullscreenRewrite = open(r"../data/fullscreen-settings.txt", "w")
    checkStateFullscreenRewrite.writelines(str(StateFullscreen))
    checkStateFullscreenRewrite.close()


def languageImport():
    checkWhatLanguage = open(r"../data/language-settings.txt", "r")
    whatLanguage = list(map(lambda x: str(x.rstrip('\n')), checkWhatLanguage))
    languageNow = whatLanguage[0]
    checkWhatLanguage.close()
    return languageNow


def languageExport(languageNow):
    checkLanguageRewrite = open(r"../data/language-settings.txt", "w")
    checkLanguageRewrite.writelines(str(languageNow))
    checkLanguageRewrite.close()


def heroImport():
    heroFile = open(r"../data/hero-settings.txt", "r", encoding="utf-8")
    checkHero = list(map(lambda x: float(x.rstrip('\n')), heroFile))
    heroNow = int(checkHero[0])
    isGetHero2 = checkHero[1]
    getHero = checkHero[2]
    heroFile.close()
    return heroNow, isGetHero2, getHero


def heroExport(hero, isGetHero2, getHero):
    checkHeroRewrite = open(r"../data/hero-settings.txt", "w")
    checkHeroRewrite.writelines([str(hero) + '\n', str(int(isGetHero2)) + '\n', str(int(getHero))])
    checkHeroRewrite.close()


def volumeImport():
    volumeFile = open(r"../data/volume-settings.txt", "r", encoding="utf-8")
    checkActDet = list(map(lambda x: float(x.rstrip('\n')), volumeFile))
    wM = checkActDet[0]
    wS = checkActDet[1]
    volS = wS
    volumeFile.close()
    return wM, wS, volS


def volumeExport(wM, wS):
    checkActDet = open(r"../data/volume-settings.txt", "w")
    checkActDet.writelines([str(wM) + '\n', str(wS)])
    checkActDet.close()
