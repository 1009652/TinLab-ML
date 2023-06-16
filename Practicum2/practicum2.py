import muser as ms
import random as rm
import numpy as np
import sys

class Composer():
    def __init__(self):
        self.notes = ms.notes
        self.fileName = "song.txt"
        self.divider = ('c8', 2)
        self.muser = ms.Muser()

    # Returns a buildingblock consisting
    # of three notes, based on a chord
    def getBuildingBlock(self) -> tuple:
        chords = {'A': ('a3', 'c#3', 'e3'), 
                  'Am': ('a3', 'c3', 'e3'),
                  'C': ('c3', 'e3', 'g3'),
                  'Cm': ('c3', 'd#3', 'g3'),
                  'D': ('d3', 'f#3', 'a4'),
                  'Dm': ('d3', 'f3', 'a4'),
                  'E': ('e3', 'g#3', 'b4'),
                  'Em': ('e3', 'g3', 'b4'),
                  'F': ('f3', 'a4', 'c4'), 
                  'Fm': ('f3', 'g#3', 'c4'),
                  'G': ('g3', 'b4', 'd4'),
                  'Gm': ('g3', 'a#4', 'd4')
                }
        return rm.choice(list(chords.values()))     

    # Returns a random note between c3 and c4
    def getRandomNote(self) -> tuple:
        note = (ms.notes[rm.randrange(27, 39)], self.getDuration())
        return note
    
    # Returns a random duration biased to the middle durations
    # (1, 2, 4, 8, 16, 32)
    def getDuration(self) -> int:
        index = 2**int(np.random.normal(3, 1))
        return index
    
    # Returns a note + duration, based on the given note 
    # and the circle of fifth's
    def getCompNote(self, note : tuple) -> tuple:
        index = self.notes.index(note[0])
        change = rm.randrange(0, 3)
        if(change == 0):
            index += 4
        elif(change == 1):
            index -= 4
        return (self.notes[(index) % len(self.notes)], note[1])
    
    # Returns a count consisting of three buildingblocks/chords
    # adds a dividing note to the end of the count
    def getCount(self) -> tuple:
        count1 = []
        count2 = []

        for i in range(3):
            chord = self.getBuildingBlock()
            duration = self.getDuration()
            for i in range(len(chord)):
                note1 = (chord[i], duration)
                note2 = self.getCompNote(note1)
                count1.append(note1)
                count2.append(note2)
        count1.append(self.divider)
        count2.append(self.divider)
        return count1, count2
    
    # Returns a random song, consisting of 5 counts
    def getGeneration0(self) -> tuple:
        count1 = []
        count2 = []
        for i in range(5):
            count = self.getCount()
            count1 += count[0]
        song = count1, count2

        return song

    # Returns a list of ratings of the song, 
    # divided into counts
    def judgeCurrentGeneration(self) -> list:
        rating = []
        for i in range(5):
            print("Rate part", i + 1)
            rating.append(int(input()))
        return rating

    # Retrieves a song, from the file and divides it into
    # the different counts, next applies the selection to it 
    # and creates one single song from the different counts.
    def getNextGeneration(self) -> tuple:
        f = open(self.fileName, "r")
        song = eval(f.read())

        oldCounts1 = []
        oldCounts2 = []
        for i in range(5):
            count1 = []
            count2 = []
            for j in range(9):
                count1.append(song[0][10*i + j])
                count2.append(song[1][10*i + j])
            oldCounts1.append(count1)
            oldCounts2.append(count2)

        counts1, counts2 = self.selection(oldCounts1, oldCounts2)

        newCounts1 = []
        newCounts2 = []
        for i in range(len(counts1)):
            counts1[i].append(self.divider)
            counts2[i].append(self.divider)
            newCounts1 += counts1[i]
            newCounts2 += counts2[i]
        song = tuple(newCounts1), tuple(newCounts2)

        return song
    
    # Applies the selection to the different counts, count1 being 
    # the first layer and count2 the second layer, takes the best
    # count and directly forwards it to the next generation, takes
    # the second best and third best and creates 4 children from
    # those counts, next applies a mutation to all the counts.
    def selection(self, counts1 : list, counts2 : list) -> tuple:
        newCounts1 = []
        newCounts2 = []

        rating = self.judgeCurrentGeneration()
        bestCount = rating.index(max(rating))
        rating.pop(bestCount)

        newCounts1.append((counts1[bestCount]))
        newCounts2.append((counts2[bestCount]))

        parentCounts1 = []
        parentCounts2 = []

        for i in range(2):
            index = rating.index(max(rating))
            rating.pop(index)
            parentCounts1.append(counts1[index])
            parentCounts2.append(counts2[index])

        for i in range(2):
            count1, count2 = self.getChildren(parentCounts1, parentCounts2)
            newCounts1 += count1
            newCounts2 += count2
        
        for i in range(len(newCounts1)):
            newCounts1[i], newCounts2[i] = self.mutate(newCounts1[i], newCounts2[i])

        return newCounts1, newCounts2

    # Creates two children from the given counts, counts1 being the first layer
    # and count2 being the second layer, both consisting of 2 counts. Randomly 
    # splits the counts and swaps their tails. so (a, b, c) and (d, e, f) with a
    # random split at 2 become (a, b, f) and (d, e, c).
    def getChildren(self, counts1 : list, counts2: list) -> tuple:
        splittingPoint = rm.randrange(1, 9)

        firstCount = counts1[0]
        secondCount = counts1[1]
        newFirstCount = firstCount[:splittingPoint] + secondCount[splittingPoint:]
        newSecondCount = secondCount[:splittingPoint] + firstCount[splittingPoint:]
        newCounts1 = [newFirstCount, newSecondCount]

        firstCount = counts2[0]
        secondCount = counts2[1]
        newFirstCount = firstCount[:splittingPoint] + secondCount[splittingPoint:]
        newSecondCount = secondCount[:splittingPoint] + firstCount[splittingPoint:]
        newCounts2 = [newFirstCount, newSecondCount]

        return newCounts1, newCounts2

    # Mutates a note with a propability of 1 in 10 or 10%, count1 being
    # the first layer, count2 the second layer. 
    def mutate(self, count1 : list, count2 : list) -> tuple:
        for i in range(len(count1)):
            if(rm.randrange(0, 10) == 0):
                #change current note
                count1[i] = self.getRandomNote()
                count2[i] = self.getCompNote(count1[i])
        return count1, count2

    # Creates the song, in 5 generations, lastly removing the dividing note
    def createSong(self, startGeneration : int = 0):
        if(startGeneration == 0):
            print("Generation 0")
            song = self.getGeneration0()
            self.createSongFile(song)
        
        for i in range(startGeneration, 5):
            print("Generation", i+1)
            song = self.getNextGeneration()    
            if(i < 4): self.createSongFile(song)    
        
        f = open(self.fileName, "r")
        song = eval(f.read())

        count1 = list(song[0])
        count2 = list(song[1])
        
        while True:
            try:
                index = count1.index(self.divider)
                count1.pop(index)
                count2.pop(index)
            except:
                break

        song = tuple(count1), tuple(count2)

        self.createSongFile(song)
        print("Final song is finished!")

    # Writes the song to the file, in case the program crashes
    def createSongFile(self, song : tuple):
        f = open(self.fileName, "w")
        f.write(str(song))
        f.close()
        self.muser.generate(song)

def main(argv):
    composer = Composer()
    try:
        composer.createSong(int(argv[0]))
    except:
        composer.createSong()

if __name__ == "__main__":
    main(sys.argv[1:])
