import graphviz as gv
from .optimizer import Optimizer

def visualize(opt: Optimizer, measurement_part=False, show_coef=True, view=True, filename="graph", title=''):
    """Visualization of SEM model via graphviz library.
    Keyword arguments:
    opt              -- A SEM Optimizer (has been optimized).
    show_coef        -- Should coefficients be visualised?
    measurement_part -- Should measurement part be visualised?
    view             -- Should graph be displayed?
    filename         -- Filename/path.
    title            -- Title.
    """
    g = gv.Digraph(format='jpg', graph_attr={'label': title})
    model = opt.model
    estimation = inspect(opt).set_index(['lval','rval'])
    
    # Structural Part
    g.node_attr.update(color='red', shape='ellipse', fontsize='25', width='2', height='1')
    for i, j in model.parameters['Beta']:
        lval, rval = model.beta_names[0][i], model.beta_names[0][j]        
        if show_coef:
            coef = str(round(estimation.loc[lval,rval]["Value"],3))
            p_value = estimation.loc[lval,rval]["P-value"]
            if p_value <= 0.01:
                coef+="***"
            elif p_value <= 0.05:
                coef+="**"
            elif p_value <= 0.1:
                coef+="*"          
            g.edge(rval, lval, color='red', label=coef)
        else:
            g.edge(rval, lval, color='red')

    # Measurement Part
    if measurement_part:
        c = gv.Digraph(name='measurement_part', node_attr={'shape': 'box','color':'black','fontsize':'15','width':'1','height':'0.5'})
        for i in model.first_indicators:
            c.edge(i, model.first_indicators[i], label="1", style="dashed")
        for i, j in model.parameters['Lambda']:
            rval, lval= model.lambda_names[0][i], model.lambda_names[1][j]
            if show_coef:
                coef = str(round(estimation.loc[lval,rval]["Value"],3))
                p_value = estimation.loc[lval,rval]["P-value"]
                if p_value <= 0.01:
                    coef+="***"
                elif p_value <= 0.05:
                    coef+="**"
                elif p_value <= 0.1:
                    coef+="*"
                c.edge(lval, rval, label=coef)
            else:
                c.edge(lval, rval)
        g.subgraph(c)
    g.render(filename, view=view)
