#%%
from fractions import Fraction


# %%
f1 =Fraction(3.141592857).limit_denominator(500)

# %%
print(f1.denominator)
print(f1.numerator)

# %%
