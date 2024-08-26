# Python-Triangular-Expansion
Messing around with TEA (Triangular Expansion Algorithm) from the paper ["Efficient Computation of Visibility Polygons"](https://www.researchgate.net/publication/260873070_Efficient_Computation_of_Visibility_Polygons).

I'm sure a bunch of these examples have logical errors and poorly implemented functions. None of these actually implement the paper 1 to 1. The closest is probably Basic TEA 2 and Simplified TEA Visibility 2, but Basic TEA 2 doesn't do a number of things. I've added a few additions in some other files, Basic_TEA_2_with_CDT.py, Basic_TEA_3.py, and Basic_TEA_3_Performance.py. Basic_TEA_3_Performance is a close contender and has great performance (based on feel, no testing was done aside from fps checking)

Some of the ideas in other files could be combined with others like for example combining Simplified TEA Visibility adn Simplified TEA Visibility 2 with Basic TEA 3 Performance. I'm sure there are other good combinations you may wish to explore.

I've also implemented d-TEA (Distance-constrained Triangular Expansion Algorithm) from the paper ["Optimizing Mesh to Improve the Triangular Expansion Algorithm for Computing Visibility Regions"](https://www.researchgate.net/publication/378128105_Optimizing_Mesh_to_Improve_the_Triangular_Expansion_Algorithm_for_Computing_Visibility_Regions) in the file "Randomized_dTEA_with_Holes.py" and "Randomized_dTEA_with_Holes_2.py" again, it may have logical errors and poorly implemented functions. It should be noted I included two grid based dTEA implementations as well; one unoptimized and one optimized.

All the examples used Pygame Community Edition, except one "TEA_PySDL2.py" which uses PySDL2. 

# Randomized dTEA with Holes
![Randomized dTEA with Holes](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Randomized_dTEA_with_Holes.png)

This implementation is robust and versatile, making excellent use of triangulation and dynamic visibility expansion in a complex environment with random polygonal holes. It is well-suited for visualizing how the dynamic Triangular Expansion Algorithm (d-TEA) performs in varied and challenging environments. With some performance optimizations and edge case handling, this could serve as a strong foundation for more advanced applications in computational geometry, gaming, or robotics.
-

# Randomized dTEA with Holes 2
![Randomized dTEA with Holes 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Randomized_dTEA_with_Holes_2.png)

This version of the dynamic Triangular Expansion Algorithm (d-TEA) is robust and well-implemented, effectively handling complex environments with polygonal holes. The introduction of view edges helps control the visibility expansion and prevents redundant calculations, making the algorithm more efficient. With further optimization and additional features, such as handling dynamic environments or incorporating a field of view, this implementation could be highly effective for real-time applications in various domains, including gaming, robotics, and computational geometry.
-

# dTEA on Grid
![dTEA on Grid](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/dTEA_on_Grid.png)

This is a well-rounded and functional example of the dynamic Triangular Expansion Algorithm on a grid. It incorporates a visibility range, handles obstacles, and dynamically expands visibility through a grid of triangles.
-

# Optimized dTEA on Grid 2
![Optimized dTEA on Grid 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Optimized_dTEA_on_Grid_2.png)

This is well-optimized and incorporates significant improvements, particularly in the use of bounding boxes to optimize obstacle intersection checks. It is well-suited for real-time applications and provides a solid foundation for further enhancements, such as scalability improvements and more advanced field-of-view calculations.
-

# Basic Grid TEA
![Basic Grid TEA](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/BasicGridTEA.png)

Basic Grid TEA isn't really TEA at all. It should be called basic visibility check. It's a starting point to create a TEA implementation.
-

# Basic Grid TEA 2
![Basic Grid TEA 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/BasicGridTEA2.png)

Basic Grid TEA 2 isn't really TEA at all. It should be called basic visibility check 2. It's a more robust starting point to create a TEA implementation.
-

# Basic TEA
![Basic TEA](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA.png)

Basic TEA is a good step toward implementing a grid-based approximation of TEA. It still isn't TEA though.
-

# Basic TEA 2
![Basic TEA 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_2.png)

Basic TEA 2 represents a significant step closer to implementing the TEA and incorporates several key concepts that align with TEA. It uses Delaunay triangulation to create a mesh and checks visibility for each triangle. However it's still grid based which isn't TEA.
-

## Problems with Basic TEA 2
 - Preprocessing with Constrained Delaunay Triangulation
   - In the TEA paper, the initial preprocessing step involves using Constrained Delaunay Triangulation (CDT) instead of a simple Delaunay triangulation. This ensures that the triangulation respects the boundaries of obstacles and the grid.
   - Replace the Delaunay triangulation in triangulate_grid with CDT, which also respects obstacle boundaries.
 - Recursive Visibility Expansion
   - The paper describes a recursive method for expanding the visible area from the observer's position through the edges of the current triangle. This recursion must properly handle the visibility cone restricted by the boundary of the polygon or other obstacles.
   - Implement a recursive function that, given a triangle and an observer's position, expands visibility by checking neighboring triangles while considering visibility constraints.
 - Handle Visibility Polygons with Antennae
   - The TEA paper mentions that the visibility polygon might include antennae (long, thin regions visible from the observer). Ensure that the algorithm can detect and correctly represent these cases.
   - Modify the visibility check to include cases where multiple vertices are collinear with the observer and consider these as potential antennae.
 - Efficiency Improvements
   - The paper emphasizes efficiency, especially in handling large and complex grids. One way to enhance efficiency is to avoid redundant checks by marking triangles that have already been processed.
   - Add a mechanism to skip triangles that have already been fully processed during the recursive expansion.
 - Output Sensitivity
   - Ensure the implementation is output-sensitive, meaning that it processes only the triangles that contribute to the visible region, thereby improving runtime.
   - Implement checks to avoid unnecessary processing of triangles that do not contribute to the final visibility polygon.
 - Visualization of Visibility Cones.
   - The paper's examples visualize the expanding visibility cone as it moves from one triangle to the next. Implementing this in the visualization could help in debugging and understanding the algorithm's behavior.
   - Add a function to draw the visibility cone as it expands through triangles.
 - Handling Degenerate Cases
   - The TEA algorithm in the paper handles degenerate cases such as collinear points or overlapping edges.
   - Add edge cases handling in the triangulation and visibility checks to account for collinear points and overlapping triangles.
 - Benchmarks and Performance Testing
   - The paper discusses various scenarios (like the Norway and cathedral examples) to benchmark the algorithm's performance. Implement similar test scenarios in the code to evaluate and optimize performance.
   - Create different loadable grid configurations and measure the performance of the implementation vs other scenarios.
  
# Basic TEA 2 with CDT
![Basic TEA 2 with CDT](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_2_with_CDT.png)

This is an example of CDT using Basic_TEA_2.py as a base. It's a strong step forward and closely mirrors some of the core concepts of TEA using CDT. With some additional refinement, particularly in the recursive expansion and edge-based visibility checks, this could further align with the TEA methodology, improving both its efficiency and accuracy in computing visibility polygons.
-

# Basic TEA 3
![Basic TEA 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_3.png)

This is an example of handling the visibility of polygons with antennae using Basic_TEA_2_with_CDT.py as a base. It's a strong and well-rounded implementation that aligns closely with the goals of TEA in computational geometry. It's quite advanced and demonstrates a good understanding of the concepts behind TEA and CDT. By focusing on recursive visibility expansion and optimizing the visibility checks, it's possible to make this implementation even more efficient and capable of handling more complex environments.
-

# Basic TEA 3 Performance
![Basic TEA 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_3_Performance.png)

This is an example of better performance with using Basic_TEA_3.py as a base. It's a very strong and capable implementation that aligns closely with the principles of TEA and Constrained Delaunay Triangulation. It efficiently computes visibility polygons in a grid-based environment, and with some additional refinements, it could become even more accurate and efficient. This implementation demonstrates a deep understanding of the core concepts and provides a solid foundation for further experimentation and improvement.
-

# Simplified TEA Visibility
![Simplified TEA Visibility](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simplified_TEA_Visibility.png)

This implementation represents a more advanced approach to visibility determination using TEA. However, there are areas where further development and optimization are needed, particularly in handling visibility through shared edges and ensuring that the algorithm scales well with more complex environments.
-

# Simplified TEA Visibility 2
![Simplified TEA Visibility 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simplified_TEA_Visibility_2.png)

This implementation is a strong example of applying TEA to a grid-based environment, with accurate and real-time visibility calculations. With some optimizations for performance, handling of edge cases, and additional features like field of view or range limitation, this approach could be highly effective for real-time applications in games, simulations, or other computational geometry tasks.
-

# Grid Triangulation
![Grid Triangulation](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Grid_Triangulation.png)

This leverages the power of shapely to manage geometric operations, which significantly simplifies the development process and improves reliability. However shapely is slow, possibly too slow for real time visibility polygons.
-

# Raycast Grid Visibility
![Raycast_Grid_Visibility](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility.png)

This implementation is an effective and straightforward approach to computing visibility in a grid-based environment using raycasting. It is well-suited for scenarios where the environment is relatively simple and where performance is less of a concern. For more complex scenarios or larger grids, you might consider implementing optimizations or alternative algorithms to improve performance and accuracy.
-

# Raycast Grid Visibility 2
![Raycast_Grid_Visibility 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility_2.png)

This implementation is a solid example of using raycasting to compute visibility polygons in a grid environment. It is straightforward, effective for small to medium-sized grids, and provides real-time feedback through Pygame. However, there are some areas where the accuracy and performance could be improved, particularly regarding how the visibility polygon is constructed and displayed. Refining these aspects would make the implementation more robust and suitable for a wider range of applications.
-

# Raycast Grid Visibility 3
![Raycast_Grid_Visibility 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility_3.png)

This implementation is a strong and versatile approach to computing visibility in a grid-based environment. By combining BFS with raycasting, it provides an accurate and real-time calculation of visible cells and walls from an observer’s position. With further optimizations and enhancements, such as adding a field of view or improving performance, this algorithm could be highly effective for real-time applications in gaming, robotics, and simulations.
-

# Simple Triangulation
![Simple Triangulation](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simple_Triangulation.png)

This implementation is a solid starting point for visualizing a grid and its triangular subdivision.
-
