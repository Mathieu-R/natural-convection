# natural-convection
- [X] Derive the similitude equations for natural convection from Navier-Stokes equations.    
- [ ] Resolve numerically these equations.    

### numerical resolutions
We use Runge-Kutta 4 and the Shooting method (which use itself Newton method to find the root)

Shooting Method : https://en.wikipedia.org/wiki/Shooting_method    
Newton Method : https://en.wikipedia.org/wiki/Newton%27s_method    
Shooting example in Python : https://nicoguaro.github.io/posts/numerical-20/    

### usage (virtual env)
```
$ chmod +x setup.sh start.sh
$ ./setup.sh
$ ./start.sh
```

### usage (if the above method does not work)
```
$ chmod +x easy_launch.sh
$ ./easy_launch.sh
```

> If you get this kind of error: _prompt\_toolkit error_
```
$ pip3 install prompt_toolkit==1.0.14
```

### documentation

Shooting method : https://kyleniemeyer.github.io/ME373-book/bvps/shooting-method.html     
Flat Plate : https://nbviewer.jupyter.org/github/Jpescudero/Laminar-Thermal-Flat-Plate/blob/master/Flat_Plate_Notebook.html    
Similiarity solution for boundary layer : https://www.sciencedirect.com/science/article/pii/S2090447912000858    
