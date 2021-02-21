#version 330

out vec4 colour;

in vec3 frag_pos;  
in vec3 frag_normal;  
in vec4 frag_colour;

uniform vec3 lightPos; 
uniform vec3 viewPos;
uniform vec3 lightColour;
uniform float wireframe;
uniform float fade;

void main()
{
	// Ambient
	float ambientStrength = 0.3f;

	vec3 ambient = ambientStrength * lightColour;
  	
	// Diffuse 
	vec3 norm = normalize(frag_normal);
	vec3 lightDir = normalize(lightPos - frag_pos);
	float diff = max(dot(norm, lightDir), 0.0);
	vec3 diffuse = diff * lightColour;
    
	// Specular
	float specularStrength = 0.9f;
	vec3 viewDir = normalize(viewPos - frag_pos);
	vec3 reflectDir = reflect(-lightDir, norm);  
	float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
	vec3 specular = specularStrength * spec * lightColour; 

	vec3 result = (ambient + diffuse + specular) * frag_colour.rgb;

    float dist = distance(viewPos, frag_pos);
 
	float opacity = clamp(dist / 50.0f, 0.0f, 1.0f) * fade;

	colour = vec4(result * wireframe, frag_colour.a - opacity);
}