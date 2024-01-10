
class Sort: 

    def __init__(self, arr): 
        self.arr = arr

    def selectionSort(self): 
        
        for i in range(len(self.arr)): 
            max_index = i
            for j in range(i+1, len(self.arr)): 
                if self.arr[max_index] > self.arr[j]: 
                    max_index = j
            
            temp = self.arr[i]
            self.arr[i] = self.arr[max_index]
            self.arr[max_index] = temp
            
        return self.arr
    
    def bubbleSort(self): 
        
        for i in range(len(self.arr)): 
            for j in range(len(self.arr)-1-i): 
                if self.arr[j] > self.arr[j+1]: 
                    temp = self.arr[j]
                    self.arr[j] = self.arr[j+1]
                    self.arr[j+1] = temp
                
        return self.arr


if __name__ == "__main__": 

    pass 
    