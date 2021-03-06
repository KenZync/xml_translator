#-*- coding: UTF-8 -*-
import re
import os
import sys
import string
import codecs
import html
from googletrans import Translator
# import translators as ts
# from translate import Translator as Translator2
from GoogleFreeTrans import Translator as Translator2
# from deep_translator import YandexTranslator

def findvalue(text):      
    matches = re.findall(r'value=\"(.+?)\"', text)
    # results
    # matches is now ['String 1', 'String 2', 'String3']
    return ",".join(matches)

def TO_UNESCAPE(text):
      # replaced = text.replace('&quot;',"'")
      # replaced = text.replace('&apos;', '"')
      # replaced = text.replace('&gt;',">")
      # replaced = text.replace('&lt;',"<")
      # replaced = text.replace('&amp;',"&")
      replaced = html.unescape(text)
      # replaced = text.translate(str.maketrans({'&gt;':">",'&lt;':"<","&apos;":"'", "&quot;":'"'}))   

      return replaced

def TO_ESCAPE_TEXT(text):
      # replaced = text.replace("&",'&amp;')
      replaced = text.translate(str.maketrans({">":'&gt;',"<":'&lt;',"'":"&apos;", '"':"&quot;"}))     
      # replaced = html.escape(text)
      # replaced = text.replace("&",'@A@')
      # replaced = text.replace("'",'@B@')
      # replaced = text.replace('"','@C@')
      # replaced = text.replace(">",'@D@')
      # replaced = text.replace("<",'@E@')      
      return replaced
# to_escape_text_table = {
#      "&": "&amp;",
#      '"': "&quot;",
#      "'": "&apos;",
#      ">": "&gt;",
#      "<": "&lt;",
#      }  
# to_escape_table = {
#      "&amp;": "&",
#      "&quot;": '"',
#      "&apos;": "'",
#      "&gt;": ">",
#      "&lt;": "<",
#      }           
# def to_escape_text(text):
#       return "".join(to_escape_text_table.get(c,c) for c in text)

# def to_escape(text):
#       return "".join(to_escape_table.get(c,c) for c in text)

def main():
      READLIMITS = 1000
      if len(sys.argv) == 3:
            print("===TRANSLATING EVERY XML FILES===")
            SOURCE_LANGUAGE = sys.argv[1]
            DESTINATION_LANGUAGE = sys.argv[2]
            print("\n==GETTING ORIGINAL WORDS BY LINES==")
            COUNT = 0
            translator = Translator()

            character_count = 0
            directory="output"
            if not os.path.exists(directory):
                  os.makedirs(directory)
            # All Folder Script
            for NAMEFILE in os.listdir():
                  if NAMEFILE.endswith('.xml'):
                    with codecs.open(NAMEFILE, "r", "utf-8") as fp:
                        print("\n==GETTING ORIGINAL WORDS BY LINES==")
                        COUNT = 0
                        translator = Translator()
                        character_count = 0
                        INDEX = 0
                        READING = 0
                        translatecount = 0
                        dontranslatelist = []
                        originlist = []
                        alienlist = []
                        alienlist_text = []
                        print("NameFile="+NAMEFILE)
                        num_lines = len([l for l in open(NAMEFILE,encoding="utf-8")])
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
                              character_count += len(KOREAN)
                              alienlist_text.append(KOREAN)
                              alienlist.append(TO_UNESCAPE(KOREAN))
                              # print("LINE:",TO_ESCAPE(KOREAN))
                              # print("ALIENLIST:",TO_UNESCAPE(KOREAN))
                              READING += len(KOREAN)
                              INDEX += 1

                              if(READING>READLIMITS):
                                    translatecount += 1
                                    READING = 0
                                    # print("\n##Doing Magic##") 
                                    print("Translation TO Line:" + str(INDEX) + "/" + str(num_lines) + "\n")
                                    translations = translator.translate(alienlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                                    translatedunescapelist = []
                                    translatedlist = []
                                    for translation in translations:
                                          translatedunescapelist.append(translation.text)
                                          translatedlist.append(TO_ESCAPE_TEXT(translation.text))
                                          # print("TRANSLATE:",TO_ESCAPE_TEXT(translation.text))
                                    englishpatch=[]
                                    # print(len(originlist))
                                    # print(len(alienlist_text))
                                    # print(len(translatedlist))
                                    # print(len(dontranslatelist))
                                    # print(len(alienlist))
                                    # print(len(translatedunescapelist))
                                    for origin,alien_text,translated,dontranslate,alien,translatedunescape in zip(originlist, alienlist_text, translatedlist, dontranslatelist,alienlist,translatedunescapelist):
                                          # print("OOO ",origin)
                                          # print("SSS ",alien_text)
                                          # print("AAA ",alien)
                                          # print("TAA ",translatedunescape)
                                          # print("TTT ",translated)
                                          # print("XXX" ,dontranslate)
                                          if(dontranslate == False):
                                                if(alien_text==TO_ESCAPE_TEXT(translated) and len(alien_text)>1 and not alien_text.isnumeric()):
                                                      while True:
                                                            try:     
                                                                  print("GO FIX: ",alien) 
                                                                  fixtranslator = Translator2.translator(src=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE).translate(alien)
                                                                  englishpatch.append(origin.replace(alien_text,TO_ESCAPE_TEXT(fixtranslator)))
                                                                  print("FIX DONE")
                                                            except AttributeError:
                                                                  continue
                                                            break
                                                else:
                                                      englishpatch.append(origin.replace(alien_text, TO_ESCAPE_TEXT(translated)))
                                          else:
                                                englishpatch.append(origin)
                                    print("\n==END MINI PART==") 

                                    
                                    # PATCH = "".join(englishpatch)
                                    
                                    file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                                    # file.write(PATCH)
                                    for finished in englishpatch:
                                          file.write(finished)
                                    file.close()
                                    dontranslatelist = []
                                    originlist = []
                                    alienlist = []   
                                    alienlist_text = []
                                    englishpatch = []
                                    translatedlist = []  
                        if originlist:
                              translatecount += 1
                              READING = 0
                              # print("\n##Doing Magic##") 
                              print("Translation Line:" + str(INDEX) + "/" + str(num_lines) + "\n")
                              translations = translator.translate(alienlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                              translatedunescapelist = []
                              translatedlist = []
                              for translation in translations:
                                    translatedunescapelist.append(translation.text)
                                    translatedlist.append(TO_ESCAPE_TEXT(translation.text))
                                    # print("TRANSLATE:",TO_ESCAPE_TEXT(translation.text))
                              englishpatch=[]
                              # print(len(originlist))
                              # print(len(alienlist_text))
                              # print(len(translatedlist))
                              # print(len(dontranslatelist))
                              # print(len(alienlist))
                              # print(len(translatedunescapelist))
                              for origin,alien_text,translated,dontranslate,alien,translatedunescape in zip(originlist, alienlist_text, translatedlist, dontranslatelist,alienlist,translatedunescapelist):
                                    # print("OOO ",origin)
                                    # print("SSS ",alien_text)
                                    # print("AAA ",alien)
                                    # print("TAA ",translatedunescape)
                                    # print("TTT ",translated)
                                    # print("XXX" ,dontranslate)
                                    if(dontranslate == False):
                                          
                                          if(alien_text==TO_ESCAPE_TEXT(translated) and len(alien_text)>1 and not alien_text.isnumeric()):
                                                while True:
                                                      try:     
                                                            print("GO FIX: ",alien) 
                                                            fixtranslator = Translator2.translator(src=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE).translate(alien)
                                                            englishpatch.append(origin.replace(alien_text,TO_ESCAPE_TEXT(fixtranslator)))
                                                            print("FIX DONE")
                                                      except AttributeError:
                                                            continue
                                                      break
                                          else:
                                                englishpatch.append(origin.replace(alien_text, TO_ESCAPE_TEXT(translated)))
                                    else:
                                          englishpatch.append(origin)
                              print("\n==END MINI PART==") 

                              
                              # PATCH = "".join(englishpatch)
                              
                              file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                              # file.write(PATCH)
                              for finished in englishpatch:
                                    file.write(finished)
                              file.close()
                              dontranslatelist = []
                              originlist = []
                              alienlist = []   
                              alienlist_text = []
                              englishpatch = []
                              translatedlist = []            
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
      COUNT = 0
      translator = Translator()
      character_count = 0
      INDEX = 0
      READING = 0
      translatecount = 0
      dontranslatelist = []
      originlist = []
      alienlist = []
      alienlist_text = []
      print("NameFile="+NAMEFILE)

      directory="output"
      if not os.path.exists(directory):
         os.makedirs(directory)

      file = codecs.open("output/"+NAMEFILE, "w","utf-8")
      file.close()
      num_lines = len([l for l in open(NAMEFILE,encoding="utf-8")])
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
                  character_count += len(KOREAN)
                  alienlist_text.append(KOREAN)
                  alienlist.append(TO_UNESCAPE(KOREAN))
                  # print("LINE:",TO_ESCAPE(KOREAN))
                  # print("ALIENLIST:",TO_UNESCAPE(KOREAN))
                  READING += len(KOREAN)
                  INDEX += 1

                  if(READING>READLIMITS):
                        translatecount += 1
                        READING = 0
                        # print("\n##Doing Magic##") 
                        print("Translation Line:" + str(INDEX) + "/" + str(num_lines) + "\n")
                        translations = translator.translate(alienlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                        translatedunescapelist = []
                        translatedlist = []
                        for translation in translations:
                              translatedunescapelist.append(translation.text)
                              translatedlist.append(TO_ESCAPE_TEXT(translation.text))
                              # print("TRANSLATE:",TO_ESCAPE_TEXT(translation.text))
                        englishpatch=[]
                        # print(len(originlist))
                        # print(len(alienlist_text))
                        # print(len(translatedlist))
                        # print(len(dontranslatelist))
                        # print(len(alienlist))
                        # print(len(translatedunescapelist))
                        for origin,alien_text,translated,dontranslate,alien,translatedunescape in zip(originlist, alienlist_text, translatedlist, dontranslatelist,alienlist,translatedunescapelist):
                              # print("OOO ",origin)
                              # print("SSS ",alien_text)
                              # print("AAA ",alien)
                              # print("TAA ",translatedunescape)
                              # print("TTT ",translated)
                              # print("XXX" ,dontranslate)
                              if(dontranslate == False):
                                    if(alien_text==TO_ESCAPE_TEXT(translated) and len(alien_text)>1 and not alien_text.isnumeric()):
                                          while True:
                                                try:     
                                                      print("GO FIX: ",alien) 
                                                      fixtranslator = Translator2.translator(src=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE).translate(alien)
                                                      englishpatch.append(origin.replace(alien_text,TO_ESCAPE_TEXT(fixtranslator)))
                                                      print("FIX DONE")
                                                except AttributeError:
                                                      continue
                                                break
                                    else:
                                          englishpatch.append(origin.replace(alien_text, TO_ESCAPE_TEXT(translated)))
                              else:
                                    englishpatch.append(origin)
                        print("\n==END MINI PART==") 

                        
                        # PATCH = "".join(englishpatch)
                        
                        file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                        # file.write(PATCH)
                        for finished in englishpatch:
                              file.write(finished)
                        file.close()
                        dontranslatelist = []
                        originlist = []
                        alienlist = []   
                        alienlist_text = []
                        englishpatch = []
                        translatedlist = []  
            if originlist:
                  translatecount += 1
                  READING = 0
                  # print("\n##Doing Magic##") 
                  print("Translation Line:" + str(INDEX) + "/" + str(num_lines) + "\n")
                  translations = translator.translate(alienlist, sec=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE)
                  translatedunescapelist = []
                  translatedlist = []
                  for translation in translations:
                        translatedunescapelist.append(translation.text)
                        translatedlist.append(TO_ESCAPE_TEXT(translation.text))
                        # print("TRANSLATE:",TO_ESCAPE_TEXT(translation.text))
                  englishpatch=[]
                  # print(len(originlist))
                  # print(len(alienlist_text))
                  # print(len(translatedlist))
                  # print(len(dontranslatelist))
                  # print(len(alienlist))
                  # print(len(translatedunescapelist))
                  for origin,alien_text,translated,dontranslate,alien,translatedunescape in zip(originlist, alienlist_text, translatedlist, dontranslatelist,alienlist,translatedunescapelist):
                        # print("OOO ",origin)
                        # print("SSS ",alien_text)
                        # print("AAA ",alien)
                        # print("TAA ",translatedunescape)
                        # print("TTT ",translated)
                        # print("XXX" ,dontranslate)
                        if(dontranslate == False):
                              if(alien_text==TO_ESCAPE_TEXT(translated) and len(alien_text)>1 and not alien_text.isnumeric()):
                                    while True:
                                          try:     
                                                print("GO FIX: ",alien) 
                                                fixtranslator = Translator2.translator(src=SOURCE_LANGUAGE, dest=DESTINATION_LANGUAGE).translate(alien)
                                                englishpatch.append(origin.replace(alien_text,TO_ESCAPE_TEXT(fixtranslator)))
                                                print("FIX DONE")
                                          except AttributeError:
                                                continue
                                          break
                              else:
                                    englishpatch.append(origin.replace(alien_text, TO_ESCAPE_TEXT(translated)))
                        else:
                              englishpatch.append(origin)
                  print("\n==END MINI PART==") 

                  
                  # PATCH = "".join(englishpatch)
                  
                  file = codecs.open("output/"+NAMEFILE, "a", "utf-8")
                  # file.write(PATCH)
                  for finished in englishpatch:
                        file.write(finished)
                  file.close()
                  dontranslatelist = []
                  originlist = []
                  alienlist = []   
                  alienlist_text = []
                  englishpatch = []
                  translatedlist = []
      print("CharacterCounts:" + str(character_count))
      print("Translate Counts Sent:" + str(translatecount))
      print("\n===TRANSLATED===")

      
      print()

if __name__ == "__main__":
    main()