#version 330

out vec4 colour;

in vec3 frag_pos;  
in vec3 frag_normal;  
in vec3 frag_colour;
in vec3 frag_lightPos;

uniform vec3 viewPos;
uniform vec3 lightColour;
uniform float wireframe;
uniform float fade;

void main()
{
    // ambient
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColour;    
    
    // diffuse 
    vec3 norm = normalize(frag_normal);
    vec3 lightDir = normalize(frag_lightPos - frag_pos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColour;
    
    // specular
    float specularStrength = 0.7;
    vec3 viewDir = normalize(-frag_pos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColour; 
    
    vec3 result = (ambient + diffuse + specular) * frag_colour;
    
    float dist = distance(viewPos, frag_pos);
 
	float opacity = clamp(dist / 50.0f, 0.0f, 1.0f) * fade;

	colour = vec4(result * wireframe, 1.0 - opacity);
}