from rest_framework import serializers
from .models import Employee, Department, Designation

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        allow_null=True,
        required=False
    )
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(),
        allow_null=True,
        required=False
    )

    department_detail = DepartmentSerializer(source='department', read_only=True)
    designation_detail = DesignationSerializer(source='designation', read_only=True)
    
    class Meta:
        model = Employee
        # we explicitly list so you get both the PKs and the detail objects
        fields = [
            'id', 'name', 'email',
            'department', 'department_detail',
            'designation', 'designation_detail',
            'join_date',
        ]

    # optional: support ?expand=department,designation to inline them under the same key
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        qs = self.context.get('request').query_params.get('expand', '')
        if 'department' in qs.split(','):
            rep['department'] = rep.pop('department_detail')
        if 'designation' in qs.split(','):
            rep['designation'] = rep.pop('designation_detail')
        return rep