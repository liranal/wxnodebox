from PathName import *
from IniFile import *
import gettext
import locale

#dwAttr = win32file.GetFileAttributes('c:\\test.txt')
#print dwAttr

#struct LanguageStruc
#{
#    const wxChar *iso, *lang;
#    unsigned char id;
#};


#// francesco: from poedit
#// TOMAKEBETTER: francesco: better solution: get it from wxwindows itself, if possible
isoLanguages =[
    ['af', 'Afrikaans',         wxLANGUAGE_AFRIKAANS ],
    ['bg', 'Bulgarian',         wxLANGUAGE_BULGARIAN ],
    ['ca', 'Catalan',           wxLANGUAGE_CATALAN ],
    ['hr', 'Croatian',          wxLANGUAGE_CROATIAN ],
    ['cs', 'Czech',             wxLANGUAGE_CZECH ],
    ['da', 'Danish',            wxLANGUAGE_DANISH ],
    ['nl', 'Dutch',             wxLANGUAGE_DUTCH ],
    ['en', 'English',           wxLANGUAGE_ENGLISH ],
    ['et', 'Estonian',          wxLANGUAGE_ESTONIAN ],
    ['fr', 'French',            wxLANGUAGE_FRENCH ],
    ['ka', 'Georgian',          wxLANGUAGE_GEORGIAN ],
    ['de', 'German',            wxLANGUAGE_GERMAN ],
    ['el', 'Greek',             wxLANGUAGE_GREEK ],
    ['hu', 'Hungarian',         wxLANGUAGE_HUNGARIAN ],
    ['is', 'Icelandic',         wxLANGUAGE_ICELANDIC ],
    ['it', 'Italian',           wxLANGUAGE_ITALIAN ],
    ['ja', 'Japanese',          wxLANGUAGE_JAPANESE ],
    ['lv', 'Latvian',           wxLANGUAGE_LATVIAN ],
    ['lt', 'Lithuanian',        wxLANGUAGE_LITHUANIAN ],
    ['nb', 'Norwegian Bokmal',  wxLANGUAGE_NORWEGIAN_BOKMAL ],
    ['nn', 'Norwegian Nynorsk', wxLANGUAGE_NORWEGIAN_NYNORSK ],
    ['pl', 'Polish',            wxLANGUAGE_POLISH ],
    ['pt', 'Portuguese',        wxLANGUAGE_PORTUGUESE ],
    ['ro', 'Romanian',          wxLANGUAGE_ROMANIAN ],
    ['ru', 'Russian',           wxLANGUAGE_RUSSIAN ],
    ['sr', 'Serbian',           wxLANGUAGE_SERBIAN ],
    ['sk', 'Slovak',            wxLANGUAGE_SLOVAK ],
    ['sl', 'Slovenian',         wxLANGUAGE_SLOVENIAN ],
    ['es', 'Spanish',           wxLANGUAGE_SPANISH ],
    ['sv', 'Swedish',           wxLANGUAGE_SWEDISH ],
    ['ta', 'Tamil',             wxLANGUAGE_TAMIL ],
    ['tr', 'Turkish',           wxLANGUAGE_TURKISH ],
]

class GuiLanguage:
    def __init__ (self):
        self.m_bLangRestartReminder = True
        p = PathName ()
        strFile = p.GetIniDirectory()
        #print strFile
        #TOFIX
        strFile += '/atol.ini'
        ini = IniFile ()
        inifileloaded = False
        self.m_strCurLang = 'en'

        if ini.Load(strFile):
            inifileloaded = true
            strValue = ini.GetValue('Default', 'Language', '')
            if(strValue != ''):
                self.m_strCurLang = strValue
            else:
                #// francesco: not sure, if there exists already a translated mo file
                #// m_strCurLang = wxLANGUAGE_DEFAULT;
                self.m_strCurLang = ''
        else:
            self.m_strCurLang = ''
        self.FindLanguages ()


    def GetNativeLangName (sel, s):
        for i in isoLanguages:
            if i[0] == s:
                return i[1]
            #// not found => than Set to english
            #// wxmessagabox 'Languag not found: Set to english'
        return 'English'

    '''
    #TODO: hinein?
    #// input 'de'
    #// output wxLanguageGerman
    int GetLangIdFromIsoName (const wxChar *s)
    {
    for (int i = 0; i < sizeof (isoLanguages) / sizeof (isoLanguages[0]); ++i)
    {
        if (!strcmp (isoLanguages[i].iso, s))
        {
        return isoLanguages[i].id;
        }
    }
    #// not found => than Set to english
    wxMessageBox (_("Language not found: Set to english"));
    return wxLANGUAGE_ENGLISH;
    }

    const wxChar *GetNativeLang (int id)
    {
    // TOFIX: francesco: correcting this function
    return isoLanguages[0].lang;
    }

    // francesco: end
    '''
    def FindLanguages(self):

        #presLan_de = gettext.translation('wxpyatol', './locale', languages=[self.m_strCurLang]) # German
        #wxLocale::AddCatalogLookupPathPrefix(_T('./share/locale'));
        if (self.m_strCurLang == ''):
            self.m_strCurLang = locale.getdefaultlocale()[:2]
            try:
                gettext.translation('wxpyatol', './locale', languages=[self.m_strCurLang])
            except:
                try:
                    self.m_strCurLang = 'en'
                    gettext.translation('wxpyatol', './locale', languages=[self.m_strCurLang])
                except:
                    pass

            #if (m_locale.Init (wxLANGUAGE_DEFAULT))
            #if 0:
                #// returns for example in Austria: de_AT: we only need the first two characters
                #m_strCurLang = m_locale.GetName ().Left (2);
                #pass
            #else:
                #// set it to english
                #// no _'' for next wxMessageBox: let this string in englisch
                #wxMessageBox ('Didn't find native Language! English is set!');
                #self.m_strCurLang = 'en'
            pass
        else:
            #// bool s = m_locale.Init (GetLangIdFromIsoName (m_strCurLang));
            #m_locale.Init (GetLangIdFromIsoName (self.m_strCurLang));
            gettext.translation('wxpyatol', './locale', languages=[self.m_strCurLang])
            #pass
        #bool l = m_locale.AddCatalog('atol');

        #// extract language identifier (here /de/ or /ru/

        self.m_arStrAvailLang = []
        os.path.walk ('.', self.LookforPoFiles, self.m_arStrAvailLang)

        #print 'erg:'
        for i  in range (len (self.m_arStrAvailLang)):
            #print self.m_arStrAvailLang[i].lower()
            ind1 = self.m_arStrAvailLang[i].find ('locale') + len ('locale')
            #ind2 = self.m_arStrAvailLang[i].find ('lc_messages')
            ##// without '\' for avoiding problems with unix
            self.m_arStrAvailLang[i] = self.m_arStrAvailLang[i][ind1 + 1: ind1 + 3]
            #print self.m_arStrAvailLang[i].lower()

    def LookforPoFiles (self, list, dirname, names):
        #print '1:'
        #print dirname
        #print names
        list.extend ([os.path.join(dirname, file)  for file in names if file == 'wxpyatol.mo'])


        gettext.install('wxpyatol', './locale', unicode=False)
        CurrLang = gettext.translation('wxpyatol', './locale', languages=[self.m_strCurLang]) # German
        #presLan = gettext.translation('wxpyatol', './locale', languages=['de']) # German
        #print presLan_de
        CurrLang.install()

    def BuildMenu (self, pMenuLanguage):
        #// add Languages
        for i in range (len(self.m_arStrAvailLang)):
            pMenuLanguage.AppendRadioItem (CMD_LANGUAGE_FIRST + i, self.GetNativeLangName (self.m_arStrAvailLang[i]))
            #// select choosen language with the menu radioitem
            if self.m_arStrAvailLang[i] == self.m_strCurLang:
                pMenuLanguage.Check (CMD_LANGUAGE_FIRST+ i, True)

