import muser as ms
import random as rm
import time

class Composer():
    def __init__(self):
        self.notes = ms.notes
        self.durations = [1, 2, 4, 8, 16, 32]

    def getNote(self, prevIndex):
        index = len(self.notes)// 2
        if(prevIndex > -1):
            min = (prevIndex - 3) % len(self.notes)
            max = (prevIndex + 3) % len(self.notes)
            if(min < max):
                index = rm.randrange(min, max, 1)
            else:
                index = rm.randrange(max, min, 1)
        return self.notes[index]
    
    def getDuration(self, prevIndex):
        index = rm.randrange(1, 2)*4
        return index
    
    def getCompNote(self, note):
        index = self.notes.index(note[0])
        if(rm.randrange(0, 1) == 0):
            index += 4
        else:
            index -= 4
        return (self.notes[(index) % len(self.notes)], note[1])
    
    def getCount(self):
        length = 0
        count1 = []
        count2 = []
        lastIndex = -1
        lastIndexDur = -1
        while(length < 1):
            duration = self.getDuration(lastIndexDur)
            note1 = (self.getNote(lastIndex), duration)
            note2 = self.getCompNote(note1)

            if(length + 1/duration <= 1):
                print(note1, note2)
                lastIndex = self.notes.index(note1[0])
                lastIndexDur = self.durations.index(note1[1])
                length += 1/duration
                count1.append(note1)
                count2.append(note2)
        return (tuple)(count1), (tuple)(count2)
    
    def getSong(self):
        song = []
        count1 = ()
        count2 = ()
        for i in range(8):
            count = self.getCount()
            count1 += count[0]
            count2 += count[1]
        song = count1, count2
        return (tuple)(song)
    
composer = Composer()
muser = ms.Muser()
song = composer.getSong()
muser.generate(song)

