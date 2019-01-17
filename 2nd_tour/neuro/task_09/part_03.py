import solution
import os
    
dir_with_images = 'smiles'
test_image = '1a.jpg'
sol = solution.Solver(dir_with_images)
print(sol.predict(os.path.join(dir_with_images,test_image)))