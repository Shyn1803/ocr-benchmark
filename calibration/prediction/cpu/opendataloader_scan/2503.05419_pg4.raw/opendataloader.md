# 1.4. Objective of the Study

The current paper aims to explore the potential of φ ML (by integrating physical knowledge and constraints into artificial neural networks) to enable efficient prediction of the fatigue lifetime of high-strength concrete, explicitly considering the effects of loading sequence in non-uniform loading scenarios. An efficient surrogate model is developed by training a physics-based machine learning framework using fatigue simulations generated from a representative macro-scale anisotropic continuum damage model. The resulting surrogate model offers two key applications:

As an advanced tool for estimating cumulative fatigue damage under variable amplitude loading scenarios. It can be directly integrated into digital twin models for real-time assessment in engineering structures, eliminating the need for computationally expensive nonlinear fatigue simulations.

Integration with finite element simulations to efficiently model fatigue behavior over the lifetime of a structure. By accounting for the number of cycles and corresponding stress amplitudes at each material point, it enables precise evaluation of stiffness degradation after individual or multiple load cycles.

In this work, we focus on the first approach, developing a surrogate model for fatigue damage estimation within digital twin frameworks, offering an efficient and practical alternative to nonlinear fatigue simulations. The structure of this paper is organized as follows: Section 2 provides a summary of the anisotropic continuum

damage fatigue model used to generate the training data for the physics-based machine learning framework, along with details on its calibration and validation. Section 3 describes the development of the φ ML model, including the data generation process, the chosen architecture, the integration of physical constraints, the customized loss function, and the training procedure. In Section 4 , the results obtained using the φ ML model are presented and discussed. Comparative analyses are performed between purely data-driven models and those incorporating physical constraints, considering both large and small datasets. Section 5 extends the developed φ ML framework to accommodate arbitrary loading scenarios through a proposed algorithm. This section also includes experimental validation studies of fatigue lifetime predictions under more complex loading conditions.

# 2. Anisotropic continuum damage model

The fatigue damage modeling approach developed by [ 77 – 79 ] is selected for this study due to its computational efficiency. Its incremental formulation ensures compatibility with a wide range of fatigue loading histories, making it adaptable to complex scenarios. The model employs a stress-driven formulation that simplifies the problem to a uniaxial stress state, allowing efficient simulation of compressive loading cycles on cylindrical solids under the assumption of uniform stress distribution. This computational efficiency is critical for conducting the large number of fatigue simulations needed to train the machine learning model. Furthermore, the model effectively captures the nonlinear progression of fatigue damage and incorporates the influence of loading sequence [ 80 ] . This is achieved by replacing the conventional yield limit with an irreversibility condition, ensuring accurate representation of loading and unloading behavior. It is important to highlight that the model used in this study primarily serves as a demonstrative example to showcase the potential of physics-based machine learning. Specifically, it illustrates how advanced fatigue damage modeling knowledge can be effectively transferred into ML frameworks for efficient lifetime prediction. While this model was chosen for its simplicity and adaptability, other advanced fatigue modeling approaches [ 8 , 19 , 21 , 29 ] , could equally serve as the foundation for similar applications.

# 2.1. Model formulation

The model is based on the anisotropic damage framework, defined by the following free energy potential

$$
(1) 2
$$

where λ , µ are the Lam´ e constants and α , β , g are anisotropic material parameters. The thermodynamic conjugate forces, namely the stress tensor and the energy release rate tensor, are obtained by taking the partial derivatives of the free energy potential with respect to the associated state variables: the strain tensor ε and the second order damage tensor ω . Thus, the stress tensor is determined by

$$
0 (2) d€
$$

