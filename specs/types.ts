interface IUseCaseData {
  name: string;
  services: IServiceData[];
  repositories: IRepositoryData[];
  dto: DtoClass;
  resource: ResourceClass;
  uses: IUseCaseData[];
  extends: IUseCaseData[];
  include: IUseCaseData[];
  action: "POST"|"GET"|"PUT"|"PATCH"|"DELETE"
}
interface IServiceData {
  name: string;
  methods: IMethod[];
}

interface IRepositoryData {
  entity: string;
  methods: IMethod[];
}

interface IMethod {
  name: string;
  args: IArg[];
  type: string;
  visibility: Visibility;
}
type Visibility = "public" | "private" | "protected";
interface IArg {
  visibility: Visibility;
  name: string;
  type: string;
}

interface DtoClass{
  name: string;
  attributes: (IArg & {decorators: IDecorator[]})[];
}
interface IDecorator {
  name: string;
  message: string;
}

interface ClassData {
  name: string;
  type: "class" | "interface";
  attributes: IArg[];
  methods: IMethod[];
  aggregations: IArg[];
  compositions: IArg[];
  importList: boolean;
}

interface ResourceClass{
  name: string;
  attributes: IArg[];
}
