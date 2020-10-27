import re
import os
import sys
import codecs
from googletrans import Translator

def findvalue(text):      
    matches = re.findall(r'value=\"(.+?)\"', text)
    # results
    # matches is now ['String 1', 'String 2', 'String3']
    return ",".join(matches)

def main():
      if len(sys.argv) == 3:
            print("===TRANSLATING EVERY XML FILES===")
            SOURCE_LANGUAGE = sys.argv[1]
            DESTINATION_LANGUAGE = sys.argv[2]
            print("\n==GETTING ORIGINAL WORDS BY LINES==")
            READLIMITS = 1
            COUNT = 0
            translator = Translator()

            koreancharcount = 0
            directory="output"
            if not os.path.exists(directory):
                  os.makedirs(directory)
            # All Folder Script
            for NAMEFILE in os.listdir():
                if NAMEFILE.endswith('.xml'):
                    with codecs.open(NAMEFILE, "r", "utf-8") as fp:
                        INDEX = 0
                        READING = 0
                        translatecount = 0
                        dontranslatelist = []
                        originlist = []
                        koreanlist = []
                        didtranslate = 0
                        print("NameFile="+NAMEFILE)
                        file = codecs.open("output/"+NAMEFILE, "w", "utf-8")
                        file.close()
                        for line in fp:
                              COUNT += 1

                              # Dont Translate a Line That Contain Variable
                              if "\"h\"" in line:
                                    dontranslatelist.append(True)
                              elif  "\"hch\"" in line:
                                    dontranslatelist.append(True)
                              elif  "\"ph\"" in line:
                                    dontranslatelist.append(True)
                              else:
                                    dontranslatelist.append(False)

                              # For remove "\n"
                              # originlist.append(line.replace('>\n', '>'))
                              
                              originlist.append(line)
                              KOREAN = findvalue(line.strip())
                              koreancharcount += len(KOREAN)
                              koreanlist.append(KOREAN)
                              READING += len(KOREAN)
                              INDEX += 1

                              while True:
                                    translatecount += 1
                                    READING = 0
                                    print("\nStart New Session at Line:" + str(INDEX))
                                    print("\n==TRANSLATION IN PROCESS==") 
                                    translations = translator.translate(koreanlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                                    translatedlist = []
                                    for translation in translations:
                                          translatedlist.append(translation.text)

                                    englishpatch=[]
                                    for origin,KOREAN,translated,dontranslate in zip(originlist, koreanlist, translatedlist, dontranslatelist):
                                          if(dontranslate == False):
                                                englishpatch.append(origin.replace(KOREAN, translated))
                                          else:
                                                englishpatch.append(origin)

                                    PATCH = "".join(englishpatch)

                                    file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                                    file.write(PATCH)
                                    file.close()
                                    dontranslatelist = []
                                    originlist = []
                                    koreanlist = []
                                    if not READING>READLIMITS:
                                          break

                              print("KoreaCharCount:" + str(koreancharcount))
                              print("Translate Count:" + str(translatecount))
                              print("\n===TRANSLATED===")            
            sys.exit()
      elif  len(sys.argv) == 4:
            print("===TRANSLATING THE XML FILE===")
      else:
            print("Usage 1: \"py xml_translator.py FromLanguage ToLanguage\"")            
            print("Usage 2: \"py xml_translator.py File.xml FromLanguage ToLanguage\"")
            print("Output will be at folder /output/files.xml")            
            print("Example : py xml_translator.py file.xml ko en")
            print("Meaning : translate file.xml from Korea to English")
            sys.exit()    
            
      NAMEFILE = sys.argv[1]
      SOURCE_LANGUAGE = sys.argv[2]
      DESTINATION_LANGUAGE = sys.argv[3]
      print("\n==GETTING ORIGINAL WORDS BY LINES==")
      READLIMITS = 1
      COUNT = 0
      translator = Translator()

      koreancharcount = 0

      # All Folder Script
      # for filename in os.listdir('C:/MapleWork/String.wz'):
      #     if filename.endswith('.xml'):
      #         with open(os.path.join('C:/MapleWork/String.wz', filename),encoding="utf8") as fp:
      #             for line in fp: 

      INDEX = 0
      READING = 0
      translatecount = 0
      dontranslatelist = []
      originlist = []
      koreanlist = []
      didtranslate = 0
      print("NameFile="+NAMEFILE)

      directory="output"
      if not os.path.exists(directory):
         os.makedirs(directory)

      file = codecs.open("output/"+NAMEFILE, "w","utf-8")
      file.close()

      with open(NAMEFILE, encoding="utf8") as fp: 
            for line in fp :

                  COUNT += 1

                  # Dont Translate a Line That Contain Variable
                  if "\"h\"" in line:
                        dontranslatelist.append(True)
                  elif  "\"hch\"" in line:
                        dontranslatelist.append(True)
                  elif  "\"ph\"" in line:
                        dontranslatelist.append(True)
                  else:
                        dontranslatelist.append(False)

                  # For remove "\n"
                  # originlist.append(line.replace('>\n', '>'))
                  
                  originlist.append(line)
                  KOREAN = findvalue(line.strip())
                  koreancharcount += len(KOREAN)
                  koreanlist.append(KOREAN)
                  READING += len(KOREAN)
                  INDEX += 1

                  while True:
                        translatecount += 1
                        READING = 0
                        print("\nStart New Session at Line:" + str(INDEX))
                        print("\n==TRANSLATION IN PROCESS==") 
                        translations = translator.translate(koreanlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                        translatedlist = []
                        for translation in translations:
                              translatedlist.append(translation.text)

                        englishpatch=[]
                        for origin,KOREAN,translated,dontranslate in zip(originlist, koreanlist, translatedlist, dontranslatelist):
                              if(dontranslate == False):
                                    englishpatch.append(origin.replace(KOREAN, translated))
                              else:
                                    englishpatch.append(origin)

                        PATCH = "".join(englishpatch)

                        file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                        file.write(PATCH)
                        file.close()
                        dontranslatelist = []
                        originlist = []
                        koreanlist = []
                        if not READING>READLIMITS:
                              break

      print("KoreaCharCount:" + str(koreancharcount))
      print("Translate Count:" + str(translatecount))
      print("\n===TRANSLATED===")

if __name__ == "__main__":
    main()